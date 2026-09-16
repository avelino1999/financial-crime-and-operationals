# 🛡️ Chip — Financial Crime & Operational AML Monitoring Engine

> **Automated Anti-Money Laundering (AML) monitoring pipeline & Management Information (MI) dashboard engineered for digital wealth operations.**

---

## 📋 Non-Technical Overview (For Stakeholders & Operations Leads)

### 📌 Business Context
As a UK wealth super-app, **Chip** processes high-frequency deposits, automated micro-saves, and withdrawals across savings accounts and investment funds. Operating in FinTech requires strict, automated compliance controls to detect suspicious money movements, fulfill regulatory AML obligations, and protect the platform from financial crime—without creating friction for everyday users.

### 🎯 What This System Solves
This project implements an automated **Daily Operational AML Rule Engine**. It scans incoming transaction logs to detect high-risk activity in real time, automatically triaging suspicious cases into an operational review queue:

1. ⏱️ **Rapid Movement of Funds (Pass-Through Risk):** Flags full withdrawals occurring within **15 minutes** of a major deposit—a key sign of pass-through account misuse or money laundering.
2. 🔄 **Structuring / "Smurfing" Patterns:** Detects users making **10+ small deposits under £100** within a short period to intentionally evade single-transaction alert thresholds.
3. 🚨 **Unverified High-Value Exposure:** Catches high-value deposits (**£5,000+**) entering accounts where Identity Verification (KYC) is still **Pending** or has **Failed**.

---

## 📊 Key Operational Insights & MI Summary

* **Total Financial Exposure Identified:** **£24,852** across **28 flagged alerts**.
* **Primary Risk Vector:** Rapid Movement of Funds represented over **90%** of all flagged operational anomalies.
* **Compliance Priority:** Automated alert triaging highlights **Critical Severity Ratio (4%)** vs. **High Risk (96%)**, allowing compliance officers to instantly prioritize urgent cases.

---

## 🛠️ Technical Architecture & Stack (For Engineers & Analysts)

### Tech Stack
* **Language:** Python (`pandas`, `numpy`)
* **SQL Query Engine:** DuckDB (In-Memory Analytical Querying via SQL Window Functions & CTEs)
* **Visualization & Reporting:** Power BI (DAX Measures, Data Modeling, Conditional Formatting)
* **Storage / Formats:** CSV, `.pbix`

### System Architecture
```text
[ Synthetic FinTech Generator ] 
          │ (users.csv, transactions.csv)
          ▼
[ DuckDB Analytical Engine (sql.py) ]
  ├── Rule 1: Window Function LAG() for Rapid Withdrawals (<15 min)
  ├── Rule 2: Grouping & Aggregation for Structuring Velocity (10+ txs <£100)
  └── Rule 3: Relational Join for Unverified Deposits (KYC Pending + £5k+)
          │
          ▼
[ Output: master_fincrime_alerts.csv ]
          │
          ▼
[ Power BI MI Operations Dashboard (Viz.pbix) ]
```

## 🔍 Technical Deep Dive: The SQL Rule Logic
### 1. Rapid Movement Detection (SQL Window Function)
Uses DuckDB's LAG() window function to calculate the exact minute delta between sequential deposits and withdrawals per user:

```SQL
WITH ranked_transactions AS (
    SELECT 
        user_id, transaction_id, transaction_type, amount,
        CAST(timestamp AS TIMESTAMP) AS tx_timestamp,
        LAG(transaction_type) OVER (PARTITION BY user_id ORDER BY CAST(timestamp AS TIMESTAMP)) AS prev_tx_type,
        LAG(CAST(timestamp AS TIMESTAMP)) OVER (PARTITION BY user_id ORDER BY CAST(timestamp AS TIMESTAMP)) AS prev_tx_timestamp
    FROM 'transactions.csv'
)
SELECT * FROM ranked_transactions
WHERE transaction_type = 'Withdrawal'
  AND prev_tx_type IN ('Manual Deposit', 'Autosave Deposit')
  AND date_diff('minute', prev_tx_timestamp, tx_timestamp) <= 15;
```

## 📂 Project Repository Structure
```Plaintext
Dashboard/
│
├── README.md                 # Complete project documentation and executive summary
├── Viz.pbix                  # Interactive Power BI dashboard source file
├── Viz.pdf                   # Printable PDF report of the Power BI dashboard
├── sql.py                    # DuckDB / SQL operational AML rule engine execution script
├── import pandas as pd.py    # Synthetic FinTech dataset generator (users & transactions)
├── master_fincrime_alerts.csv # Consolidated AML risk alerts dataset
├── users.csv                 # Synthetic user profiles & KYC status dataset
└── transactions.csv          # Synthetic transaction ledger
```

## 🚀 How to Run This Project Locally
Clone the Repository:

```Bash
git clone [https://github.com/avelino1999/Dashboard.git](https://github.com/avelino1999/Dashboard.git)
cd Dashboard
```

Generate the Datasets:

```Bash
python "import pandas as pd.py"
```

Run the DuckDB AML Engine:

```Bash
python sql.py
```

This outputs master_fincrime_alerts.csv containing all flagged operational alerts.

View the Dashboard:

Open Viz.pbix in Power BI Desktop or review Viz.pdf for static report slides.
