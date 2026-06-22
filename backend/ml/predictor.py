import joblib
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

model       = joblib.load(BASE_DIR / "isolation_forest.pkl")
scaler      = joblib.load(BASE_DIR / "scaler.pkl")
FEATURES    = joblib.load(BASE_DIR / "features.pkl")
le_merchant = joblib.load(BASE_DIR / "le_merchant.pkl")
le_device   = joblib.load(BASE_DIR / "le_device.pkl")


def predict_transaction(txn: dict) -> dict:
    try:
        merchant_enc = le_merchant.transform([txn['merchant_category']])[0]
        device_enc   = le_device.transform([txn['device_type']])[0]
    except ValueError:
        merchant_enc = 0
        device_enc   = 0

    row = {
        'amount':                  txn['amount'],
        'hour_of_day':             txn['hour_of_day'],
        'day_of_week':             txn['day_of_week'],
        'is_new_receiver':         txn['is_new_receiver'],
        'txn_frequency_last_hour': txn['txn_frequency_last_hour'],
        'merchant_enc':            merchant_enc,
        'device_enc':              device_enc
    }

    X = scaler.transform(pd.DataFrame([row])[FEATURES])
    pred  = model.predict(X)[0]
    score = float(model.decision_function(X)[0])
    is_anomaly = pred == -1

    risk = 'HIGH' if score < -0.1 else 'MEDIUM' if score < 0 else 'LOW'
    return {'is_anomaly': is_anomaly, 'anomaly_score': round(score, 4), 'risk_level': risk}
