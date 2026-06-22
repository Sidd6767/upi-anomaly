from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionOut(BaseModel):
    id: int
    transaction_id: str
    sender_vpa: str
    receiver_vpa: str
    amount: float
    merchant_category: str
    hour_of_day: int
    is_anomaly: bool
    anomaly_score: float
    created_at: datetime
    class Config: orm_mode = True

class PredictRequest(BaseModel):
    amount: float
    hour_of_day: int
    day_of_week: int
    is_new_receiver: int
    txn_frequency_last_hour: int
    merchant_category: str
    device_type: str

class PredictResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    risk_level: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
