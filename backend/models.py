# Author: Ronald Wen
# models.py - SQLAlchemy ORM models for users and prediction logs

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    predictions = relationship('PredictionLog', back_populates='user')


class PredictionLog(Base):
    __tablename__ = 'prediction_logs'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    amount = Column(Float, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    prediction = Column(Boolean, nullable=False)
    shap_values = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='predictions')
