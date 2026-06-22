from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from schemas import TransactionOut

router = APIRouter()

@router.get('/', response_model=List[TransactionOut])
def get_transactions(
    limit: int = Query(50, ge=1, le=200),
    anomaly_only: bool = False,
    db: Session = Depends(get_db)
):
    q = db.query(models.Transaction).order_by(models.Transaction.id.desc())
    if anomaly_only:
        q = q.filter(models.Transaction.is_anomaly == True)
    return q.limit(limit).all()

@router.get('/stats')
def get_stats(db: Session = Depends(get_db)):
    total    = db.query(models.Transaction).count()
    anomalies= db.query(models.Transaction).filter(models.Transaction.is_anomaly == True).count()
    return {
        'total': total,
        'anomalies': anomalies,
        'anomaly_rate': round(anomalies / total * 100, 2) if total else 0
    }
