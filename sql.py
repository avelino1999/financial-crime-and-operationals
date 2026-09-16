import duckdb
import pandas as pd

print("⚡ Running DuckDB AML Operational Engine...\n")

# Query 1: Rapid Movement of Funds
q_rapid = """
WITH ranked_transactions AS (
    SELECT 
        user_id, transaction_id, transaction_type, amount,
        CAST(timestamp AS TIMESTAMP) AS tx_timestamp,
        LAG(transaction_type) OVER (PARTITION BY user_id ORDER BY CAST(timestamp AS TIMESTAMP)) AS prev_tx_type,
        LAG(amount) OVER (PARTITION BY user_id ORDER BY CAST(timestamp AS TIMESTAMP)) AS prev_amount,
        LAG(CAST(timestamp AS TIMESTAMP)) OVER (PARTITION BY user_id ORDER BY CAST(timestamp AS TIMESTAMP)) AS prev_tx_timestamp
    FROM 'transactions.csv'
)
SELECT 
    user_id,
    'Rapid Movement of Funds' AS alert_rule_name,
    'HIGH' AS operational_risk_level,
    amount AS flagged_amount,
    tx_timestamp AS alert_time,
    'New' AS alert_status
FROM ranked_transactions
WHERE transaction_type = 'Withdrawal'
  AND prev_tx_type IN ('Manual Deposit', 'Autosave Deposit')
    AND date_diff('minute', prev_tx_timestamp, tx_timestamp) <= 15
"""

# Query 2: Structuring Pattern
q_structuring = """
SELECT 
    t.user_id,
    'Structuring / Smurf Pattern' AS alert_rule_name,
    'HIGH' AS operational_risk_level,
    SUM(t.amount) AS flagged_amount,
    MAX(CAST(t.timestamp AS TIMESTAMP)) AS alert_time,
    'New' AS alert_status
FROM 'transactions.csv' t
JOIN 'users.csv' u ON t.user_id = u.user_id
WHERE t.amount < 100 AND t.transaction_type IN ('Manual Deposit', 'Autosave Deposit')
GROUP BY t.user_id
HAVING COUNT(t.transaction_id) >= 10
"""

# Query 3: Unverified High Value
q_unverified = """
SELECT 
    t.user_id,
    'Unverified High-Value Deposit' AS alert_rule_name,
    'CRITICAL' AS operational_risk_level,
    t.amount AS flagged_amount,
    CAST(t.timestamp AS TIMESTAMP) AS alert_time,
    'Under Review' AS alert_status
FROM 'transactions.csv' t
JOIN 'users.csv' u ON t.user_id = u.user_id
WHERE u.kyc_status IN ('Pending', 'Failed') 
    AND t.amount >= 5000
"""

# Union all risk flags into a single consolidated operational table
master_query = f"""
SELECT * FROM ({q_rapid})
UNION ALL
SELECT * FROM ({q_structuring})
UNION ALL
SELECT * FROM ({q_unverified});
"""

# Execute via DuckDB and export
master_alerts_df = duckdb.sql(master_query).df()
master_alerts_df.to_csv('master_fincrime_alerts.csv', index=False)

print("✅ DuckDB Execution Complete!")
print(f"Total Operational Risk Alerts Triggered: {len(master_alerts_df)}")
print("\nPreview of Flagged Alerts:")
print(master_alerts_df.head())