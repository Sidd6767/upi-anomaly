from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter()

@router.get('/by-hour')
def transactions_by_hour(db: Session = Depends(get_db)):
    results = db.query(
        models.Transaction.hour_of_day,
        func.count(models.Transaction.id).label('count'),
        func.sum(models.Transaction.is_anomaly).label('anomalies')
    ).group_by(models.Transaction.hour_of_day).all()
    return [{'hour': r.hour_of_day, 'count': r.count, 'anomalies': r.anomalies or 0}
            for r in results]

@router.get('/by-merchant')
def transactions_by_merchant(db: Session = Depends(get_db)):
    results = db.query(
        models.Transaction.merchant_category,
        func.count(models.Transaction.id).label('count'),
        func.sum(models.Transaction.is_anomaly).label('anomalies')
    ).group_by(models.Transaction.merchant_category).all()
    return [{'category': r.merchant_category, 'count': r.count, 'anomalies': r.anomalies or 0}
            for r in results]

@router.get('/score-distribution')
def score_distribution(db: Session = Depends(get_db)):
    results = db.query(models.Transaction.anomaly_score).order_by(
        models.Transaction.id.desc()).limit(200).all()
    return [{'score': r.anomaly_score} for r in results]
