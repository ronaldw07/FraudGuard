# FraudGuard

FraudGuard is a full-stack fraud detection platform that analyzes credit card transactions in real time. It uses an XGBoost classifier trained on the Kaggle Credit Card Fraud Detection dataset, wrapped in a FastAPI backend, and served through a React + TypeScript dashboard. Each prediction is explained using SHAP feature attributions, logged to PostgreSQL, and displayed with risk level badges and interactive charts.

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11 (for ML training)
- Kaggle Credit Card Fraud Detection dataset (`creditcard.csv`)

### 1. Clone the repository
```bash
git clone https://github.com/ronaldw07/FraudGuard.git
cd FraudGuard
```

### 2. Download the dataset
Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it in the `ml/` directory:
```
ml/creditcard.csv
```

### 3. Train the model
```bash
pip install -r backend/requirements.txt
python ml/train.py
python ml/evaluate.py
```

This will save `model.pkl`, `scaler.pkl`, and `threshold.json` into `backend/model/`.

### 4. Start the platform
```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Default Login

| Username | Password       |
|----------|----------------|
| demo     | fraudguard123  |

## Tech Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| ML        | XGBoost, scikit-learn, SHAP, imbalanced-learn, MLflow |
| Backend   | FastAPI, SQLAlchemy, PostgreSQL, JWT auth        |
| Frontend  | React, TypeScript, Tailwind CSS, recharts, axios |
| DevOps    | Docker, Docker Compose, GitHub Actions           |

## Author

Ronald Wen
