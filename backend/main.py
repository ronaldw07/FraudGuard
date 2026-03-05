# Author: Ronald Wen
# main.py - FastAPI application entry point

import json
import os

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import User
from routes import auth, history, predict
from routes.auth import seed_demo_user

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')


def create_app() -> FastAPI:
    app = FastAPI(title='FraudGuard API', version='1.0.0')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
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

    return app


app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
