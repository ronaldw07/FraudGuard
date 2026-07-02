# Author: Ronald Wen
# main.py - FastAPI application entry point

import json
import os

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import User
from rate_limit import limiter
from routes import auth, history, predict
from routes.auth import seed_demo_user

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    if origin.strip()
]


def create_app() -> FastAPI:
    app = FastAPI(title='FraudGuard API', version='1.0.0')

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(auth.router)
    app.include_router(predict.router)
    app.include_router(history.router)

    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(bind=engine)

        if os.getenv('SEED_DEMO_USER', 'false').lower() == 'true':
            db: Session = SessionLocal()
            try:
                seed_demo_user(db)
            finally:
                db.close()

        model_path = os.path.join(MODEL_DIR, 'model.pkl')
        scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
        threshold_path = os.path.join(MODEL_DIR, 'threshold.json')

        app.state.model = joblib.load(model_path)
        app.state.scaler = joblib.load(scaler_path)

        with open(threshold_path) as f:
            app.state.threshold = json.load(f)['threshold']

        print(f"Model loaded. Decision threshold: {app.state.threshold}")

    # Serve the built React app from the same origin (single-URL deploy).
    # Guarded so local API-only runs (docker-compose) are unaffected.
    if os.path.isdir(STATIC_DIR):
        index_file = os.path.join(STATIC_DIR, 'index.html')

        @app.get('/{full_path:path}')
        def serve_spa(full_path: str) -> FileResponse:
            requested = os.path.join(STATIC_DIR, full_path)
            if full_path and os.path.isfile(requested):
                return FileResponse(requested)
            return FileResponse(index_file)

    return app


app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
