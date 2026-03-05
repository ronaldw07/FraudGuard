# Author: Ronald Wen
# predict.py - Transaction fraud prediction endpoint

import sys
import os
from datetime import datetime

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))
import explainability

from database import get_db
from dependencies import get_current_user
from models import PredictionLog, User
from schemas import PredictionResponse, ShapFeature, TransactionInput

router = APIRouter(prefix='/predict', tags=['predict'])

FEATURE_COLS = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'Amount']


def assign_risk_level(probability: float) -> str:
    if probability < 0.3:
        return 'low'
    elif probability <= 0.7:
        return 'medium'
    return 'high'


@router.post('', response_model=PredictionResponse)
def predict(
    transaction: TransactionInput,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    model = request.app.state.model
    scaler = request.app.state.scaler
    threshold = request.app.state.threshold

    input_data = {
        'Time': transaction.Time,
        'V1': transaction.V1,
        'V2': transaction.V2,
        'V3': transaction.V3,
        'V4': transaction.V4,
        'V5': transaction.V5,
        'V6': transaction.V6,
        'V7': transaction.V7,
        'V8': transaction.V8,
        'V9': transaction.V9,
        'V10': transaction.V10,
        'Amount': transaction.Amount,
        # Remaining V columns not provided default to 0
        'V11': 0.0, 'V12': 0.0, 'V13': 0.0, 'V14': 0.0, 'V15': 0.0,
        'V16': 0.0, 'V17': 0.0, 'V18': 0.0, 'V19': 0.0, 'V20': 0.0,
        'V21': 0.0, 'V22': 0.0, 'V23': 0.0, 'V24': 0.0, 'V25': 0.0,
        'V26': 0.0, 'V27': 0.0, 'V28': 0.0,
    }

    all_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    input_df = pd.DataFrame([input_data])[all_cols]

    # Scale Time and Amount
    input_df[['Time', 'Amount']] = scaler.transform(input_df[['Time', 'Amount']])

    fraud_probability = float(model.predict_proba(input_df)[:, 1][0])
    is_fraud = fraud_probability >= threshold
    risk_level = assign_risk_level(fraud_probability)

    shap_result = explainability.get_shap_values(input_df)
    top_features = shap_result['top_features']

    log = PredictionLog(
        timestamp=datetime.utcnow(),
        amount=transaction.Amount,
        fraud_probability=fraud_probability,
        risk_level=risk_level,
        prediction=is_fraud,
        shap_values=top_features,
        user_id=current_user.id,
    )
    db.add(log)
    db.commit()

    shap_features = [
        ShapFeature(
            feature=f['feature'],
            shap_value=f['shap_value'],
            direction=f['direction'],
        )
        for f in top_features
    ]

    return PredictionResponse(
        fraud_probability=fraud_probability,
        risk_level=risk_level,
        prediction=is_fraud,
        shap_values=shap_features,
    )
