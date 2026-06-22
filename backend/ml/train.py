import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os
import sys
sys.path.append('..')
from ml.generator import generate_dataset

df = generate_dataset(n=10000, anomaly_ratio=0.02)

le_merchant = LabelEncoder()
le_device   = LabelEncoder()
df['merchant_enc'] = le_merchant.fit_transform(df['merchant_category'])
df['device_enc']   = le_device.fit_transform(df['device_type'])

FEATURES = ['amount','hour_of_day','day_of_week','is_new_receiver',
            'txn_frequency_last_hour','merchant_enc','device_enc']

X = df[FEATURES]
y = df['is_anomaly']
X_normal = X[y == 0]

scaler = StandardScaler()
X_normal_scaled = scaler.fit_transform(X_normal)

model = IsolationForest(n_estimators=200, contamination=0.02, random_state=42, n_jobs=-1)
model.fit(X_normal_scaled)

os.makedirs('ml', exist_ok=True)
joblib.dump(model,       'isolation_forest.pkl')
joblib.dump(scaler,      'scaler.pkl')
joblib.dump(FEATURES,    'features.pkl')
joblib.dump(le_merchant, 'le_merchant.pkl')
joblib.dump(le_device,   'le_device.pkl')
print('Model trained and saved.')
