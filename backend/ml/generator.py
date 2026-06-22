import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('en_IN')  # Indian locale for realistic data
random.seed(42)
np.random.seed(42)

MERCHANT_CATEGORIES = ['grocery', 'fuel', 'restaurant', 'ecommerce',
                        'utility', 'travel', 'medical', 'entertainment']

DEVICE_TYPES = ['android', 'ios', 'feature_phone']

def generate_normal_transaction():
    hours = list(range(8, 23))
    probs = np.array([4,6,8,10,10,9,9,8,8,7,7,6,5,4,9])
    probs = probs / probs.sum()

    hour = int(np.random.choice(hours, p=probs))
    amount = np.random.lognormal(mean=6.5, sigma=1.2)  # realistic INR amounts
    amount = min(max(amount, 10), 50000)  # clip between 10 and 50000
    return {
        'transaction_id': f'UPI{random.randint(1000000000, 9999999999)}',
        'sender_vpa': f'{fake.user_name()}@upi',
        'receiver_vpa': f'{fake.user_name()}@{random.choice(["okaxis","oksbi","ybl","paytm"])}',
        'amount': round(amount, 2),
        'hour_of_day': hour,
        'day_of_week': random.randint(0, 6),
        'merchant_category': random.choice(MERCHANT_CATEGORIES),
        'device_type': random.choice(DEVICE_TYPES),
        'is_new_receiver': random.choices([0, 1], weights=[0.85, 0.15])[0],
        'txn_frequency_last_hour': random.randint(0, 3),
        'is_anomaly': 0
    }

def generate_anomaly():
    txn = generate_normal_transaction()
    anomaly_type = random.choice(['large_amount', 'odd_hour', 'high_frequency', 'new_receiver_large'])
    if anomaly_type == 'large_amount':
        txn['amount'] = round(random.uniform(80000, 200000), 2)
    elif anomaly_type == 'odd_hour':
        txn['hour_of_day'] = random.choice([1, 2, 3, 4])
        txn['amount'] = round(random.uniform(5000, 30000), 2)
    elif anomaly_type == 'high_frequency':
        txn['txn_frequency_last_hour'] = random.randint(15, 30)
    elif anomaly_type == 'new_receiver_large':
        txn['is_new_receiver'] = 1
        txn['amount'] = round(random.uniform(20000, 100000), 2)
    txn['is_anomaly'] = 1
    return txn

def generate_dataset(n=10000, anomaly_ratio=0.02):
    n_anomaly = int(n * anomaly_ratio)
    n_normal = n - n_anomaly
    data = [generate_normal_transaction() for _ in range(n_normal)]
    data += [generate_anomaly() for _ in range(n_anomaly)]
    df = pd.DataFrame(data).sample(frac=1).reset_index(drop=True)
    return df

if __name__ == '__main__':
    df = generate_dataset(10000)
    print(df.head())
