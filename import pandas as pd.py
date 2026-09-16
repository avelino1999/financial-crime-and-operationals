import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# --- 1. GENERATE USERS ---
num_users = 200
user_ids = [f"USR_{1000 + i}" for i in range(num_users)]
kyc_statuses = np.random.choice(['Verified', 'Pending', 'Failed'], size=num_users, p=[0.85, 0.12, 0.03])
risk_scores = np.random.choice(['Low', 'Medium', 'High'], size=num_users, p=[0.75, 0.20, 0.05])

users_df = pd.DataFrame({
    'user_id': user_ids,
    'signup_date': [datetime(2026, 1, 1) + timedelta(days=random.randint(0, 60)) for _ in range(num_users)],
    'kyc_status': kyc_statuses,
    'risk_score': risk_scores
})

# --- 2. GENERATE TRANSACTIONS ---
transactions = []
tx_id_counter = 10000

for idx, user in users_df.iterrows():
    u_id = user['user_id']
    base_time = user['signup_date'] + timedelta(days=random.randint(1, 10))
    
    # Normal User Transactions
    num_tx = random.randint(3, 10)
    for _ in range(num_tx):
        tx_time = base_time + timedelta(hours=random.randint(1, 48))
        amount = round(random.uniform(10, 250), 2)
        tx_type = random.choice(['Autosave Deposit', 'Manual Deposit', 'Withdrawal'])
        transactions.append([f"TX_{tx_id_counter}", u_id, tx_time, amount, tx_type, 'Completed'])
        tx_id_counter += 1

# --- 3. INJECT ANOMALIES (FINCRIME PATTERNS) ---

# Anomaly 1: Rapid Movement of Funds (User USR_1005)
rapid_user = "USR_1005"
dep_time = datetime(2026, 2, 10, 14, 0, 0)
transactions.append([f"TX_{tx_id_counter}", rapid_user, dep_time, 7500.00, 'Manual Deposit', 'Completed'])
tx_id_counter += 1
transactions.append([f"TX_{tx_id_counter+1}", rapid_user, dep_time + timedelta(minutes=6), 7500.00, 'Withdrawal', 'Completed'])
tx_id_counter += 2

# Anomaly 2: Structuring / Micro-Deposits (User USR_1012)
struct_user = "USR_1012"
struct_time = datetime(2026, 2, 15, 9, 0, 0)
for i in range(12):
    transactions.append([f"TX_{tx_id_counter}", struct_user, struct_time + timedelta(minutes=i*4), 95.00, 'Manual Deposit', 'Completed'])
    tx_id_counter += 1

# Anomaly 3: High-Value Unverified Account (User USR_1040 - Pending KYC)
users_df.loc[users_df['user_id'] == 'USR_1040', 'kyc_status'] = 'Pending'
unver_time = datetime(2026, 2, 18, 11, 0, 0)
transactions.append([f"TX_{tx_id_counter}", 'USR_1040', unver_time, 12500.00, 'Manual Deposit', 'Completed'])

# Compile and Save CSVs
tx_df = pd.DataFrame(transactions, columns=['transaction_id', 'user_id', 'timestamp', 'amount', 'transaction_type', 'status'])

users_df.to_csv('users.csv', index=False)
tx_df.to_csv('transactions.csv', index=False)

print("✅ Data successfully generated: 'users.csv' and 'transactions.csv' created.")