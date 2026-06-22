from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id               = Column(Integer, primary_key=True, index=True)
    transaction_id   = Column(String, unique=True, index=True)
    sender_vpa       = Column(String)
    receiver_vpa     = Column(String)
    amount           = Column(Float)
    merchant_category= Column(String)
    hour_of_day      = Column(Integer)
    day_of_week      = Column(Integer)
    is_new_receiver  = Column(Integer)
    txn_frequency    = Column(Integer)
    is_anomaly       = Column(Boolean, default=False)
    anomaly_score    = Column(Float)
    created_at       = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = 'users'
    id             = Column(Integer, primary_key=True, index=True)
    username       = Column(String, unique=True, index=True)
    hashed_password= Column(String)
    created_at     = Column(DateTime, server_default=func.now())
