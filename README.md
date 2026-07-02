# FraudGuard

**Real-time credit-card fraud detection with explainable ML.** A full-stack platform that scores transactions with an XGBoost model, explains *why* each one was flagged using SHAP feature attributions, and serves it all through an authenticated React dashboard.

🔗 **Live demo:** _add your Railway URL here after deploying_ — log in with `demo` / `fraudguard123`

<!-- Add a screenshot or GIF here — recruiters look at this first.
     ![FraudGuard dashboard](docs/screenshot.png) -->

---

## What it does

1. A user submits a transaction (Time, Amount, and PCA features V1–V28) through the React form.
2. The FastAPI backend scales the inputs with the saved `StandardScaler` and runs `XGBoost.predict_proba`.
3. If fraud probability clears the tuned decision threshold, it's flagged.
4. A SHAP `TreeExplainer` computes the top feature contributions behind the decision.
5. The result and its explanation are logged to PostgreSQL and rendered as a risk badge, probability, and an interactive SHAP chart.

## Architecture

```
React + TS (Vite)  ──►  FastAPI  ──►  XGBoost + SHAP
    dashboard          JWT auth        (in-process)
                          │
                          ▼
                     PostgreSQL
                  (users, prediction logs)
```

In production the React build is served **by the FastAPI app itself** as a single container, so the whole platform runs behind one URL — no CORS, no separate frontend host.

## Key engineering decisions

- **Threshold tuning, not the 0.5 default** — the decision threshold (0.85) was selected by sweeping F1 scores across 0.1–0.9, since fraud is a heavily imbalanced problem where the naive cutoff performs poorly.
- **SMOTE at `sampling_strategy=0.1`** rather than full class balance — enough minority oversampling to help recall without exploding the 284K-row dataset in memory.
- **XGBoost with `tree_method='hist'`** for memory-efficient training.
- **Only Time and Amount are scaled** — V1–V28 are already PCA-transformed, so re-scaling them would distort the components.
- **Explainability built in** — every prediction ships with its top SHAP contributions, so the model isn't a black box.

## Production considerations

- **Auth:** JWT bearer tokens, bcrypt-hashed passwords. The signing secret is required at startup (the app refuses to boot without `JWT_SECRET`) — no insecure fallback.
- **Rate limiting:** per-IP limits via `slowapi` — `30/min` on inference and `10/min` on login to blunt brute-force attempts.
- **Config:** all secrets and origins are environment-driven; nothing sensitive is committed.

## Tech stack

| Layer    | Technology                                             |
|----------|--------------------------------------------------------|
| ML       | XGBoost, scikit-learn, SHAP, imbalanced-learn, MLflow  |
| Backend  | FastAPI, SQLAlchemy, PostgreSQL, JWT, slowapi          |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Recharts, axios |
| Deploy   | Docker (single-image build), Render, Neon (Postgres)    |

---

## Run it locally

**Prerequisites:** Docker + Docker Compose, and the [Kaggle Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).

```bash
git clone https://github.com/ronaldw07/FraudGuard.git
cd FraudGuard

# 1. Add the dataset and train the model (produces backend/model/*.pkl)
#    Place creditcard.csv at ml/creditcard.csv first.
pip install -r backend/requirements.txt -r ml/requirements-train.txt
python ml/preprocessing.py
python ml/train.py
python ml/evaluate.py

# 2. Start the full stack
docker-compose up --build
```

- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs
- Login: `demo` / `fraudguard123`

## Deploy (single URL, free tier)

The repo builds to one image ([`docker/Dockerfile.web`](docker/Dockerfile.web)) where FastAPI serves the React build, so the whole platform runs as one Render web service on one URL.

1. Create a free Postgres database at [neon.tech](https://neon.tech) and copy its connection string.
2. On [Render](https://render.com): **New -> Blueprint**, connect this repo. Render reads [`render.yaml`](render.yaml) and provisions the service automatically.
3. When prompted for `DATABASE_URL`, paste the Neon connection string. `JWT_SECRET` is auto-generated; `SEED_DEMO_USER` is already set.
4. Once it deploys, Render gives you a public `*.onrender.com` URL — that's your live link.

Note: Render's free tier spins the service down after 15 minutes of inactivity; the next request takes ~30-50s to wake it back up.

## Author

Ronald Wen
