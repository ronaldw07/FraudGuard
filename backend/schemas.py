# Author: Ronald Wen
# schemas.py - Pydantic request and response schemas

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, field_serializer


class TransactionInput(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    Amount: float


class ShapFeature(BaseModel):
    feature: str
    shap_value: float
    direction: str


class PredictionResponse(BaseModel):
    fraud_probability: float
    risk_level: str
    prediction: bool
    shap_values: List[ShapFeature]


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PredictionHistoryItem(BaseModel):
    id: int
    timestamp: datetime
    amount: float
    fraud_probability: float
    risk_level: str
    prediction: bool

    class Config:
        from_attributes = True

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime, _info) -> str:
        # Stored timestamps are naive UTC (datetime.utcnow()) — attach the
        # offset explicitly so clients don't misparse it as local time.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
