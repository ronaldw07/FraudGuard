# Author: Ronald Wen
# history.py - Prediction history endpoint

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import PredictionLog, User
from schemas import PredictionHistoryItem

router = APIRouter(prefix='/history', tags=['history'])


@router.get('', response_model=List[PredictionHistoryItem])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = (
        db.query(PredictionLog)
        .filter(PredictionLog.user_id == current_user.id)
        .order_by(PredictionLog.timestamp.desc())
        .limit(50)
        .all()
    )
    return logs
