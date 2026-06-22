from unittest import result

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading, time, random
from database import engine, SessionLocal
import models
from ml.generator import generate_normal_transaction, generate_anomaly
from ml.predictor import predict_transaction
import routers.transactions as transactions
import routers.analytics as analytics
import routers.predict as predict
import routers.auth as auth
# Create DB tables
models.Base.metadata.create_all(bind=engine)

# ── BACKGROUND TRANSACTION GENERATOR ──────────────────────────
def transaction_worker():
    """Runs in background thread. Generates + scores 1 transaction/sec."""
    while True:
        try:
            txn = generate_anomaly() if random.random() < 0.05 else generate_normal_transaction()
            result = predict_transaction(txn)

            db = SessionLocal()
            db_txn = models.Transaction(
                transaction_id    = str(txn['transaction_id']),
                sender_vpa        = str(txn['sender_vpa']),
                receiver_vpa      = str(txn['receiver_vpa']),
                amount            = float(txn['amount']),
                merchant_category = str(txn['merchant_category']),
                hour_of_day=int(txn["hour_of_day"]),
                day_of_week=int(txn["day_of_week"]),
                is_new_receiver=int(txn["is_new_receiver"]),
                txn_frequency=int(txn["txn_frequency_last_hour"]),
                anomaly_score=float(result["anomaly_score"]),
            )
            db.add(db_txn)
            db.commit()
            db.close()
        except Exception as e:
            print(f'Worker error: {e}')
        time.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background thread on startup
    t = threading.Thread(target=transaction_worker, daemon=True)
    t.start()
    print('Transaction worker started.')
    yield

app = FastAPI(title='UPI Anomaly Detection API', lifespan=lifespan)

# CORS -- allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'https://your-vercel-app.vercel.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router,         prefix='/auth',         tags=['Auth'])
app.include_router(transactions.router, prefix='/transactions', tags=['Transactions'])
app.include_router(analytics.router,    prefix='/analytics',    tags=['Analytics'])
app.include_router(predict.router,      prefix='/predict',      tags=['Predict'])

@app.get('/')
def root(): return {'status': 'UPI Anomaly Detection API live'}
