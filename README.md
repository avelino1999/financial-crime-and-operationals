# 🛡️ Chip - Financial Crime & Operational AML Monitoring Engine

## 📌 Executive Summary
Chip operates as a digital wealth app handling large volumes of user deposits, autosaves, and withdrawals via Open Banking. To mitigate financial crime exposure and ensure compliance control, this project implements an **automated SQL/DuckDB operational monitoring engine** that detects suspicious transactions and outputs daily Management Information (MI) metrics.

---

## 🎯 Business Problem & Key Risks
Without automated daily operational controls, financial crime risks can pass through undetected, leading to regulatory fines and financial losses. This project detects three high-impact risk scenarios:

1. **Rapid Movement of Funds:** Instant withdrawals happening within $<15$ minutes of a major deposit (pass-through account activity).
2. **Structuring / Smurfing Pattern:** Users making 10+ micro-deposits under £100 to bypass single-transaction threshold alerts.
3. **Unverified High-Value Deposits:** Accounts accumulating $\ge$ £5,000 while Identity Verification (KYC) status is `Pending` or `Failed`.

---

## 🛠️ Architecture & Tech Stack
* **Data Synthesis:** Python (`pandas`, `numpy`) generating realistic FinTech user sign-ups and transaction logs embedded with known risk anomalies.
* **Rule Engine:** **DuckDB / SQL** utilizing Common Table Expressions (CTEs), window functions (`LAG`), and date-difference calculations to generate daily alert flags.
* **MI Dashboard:** **Power BI** interactive operational report providing real-time KPI tracking, risk breakdown, and an operational action queue.

---

## 📊 Key Insights & Dashboard Metrics
* **Total Exposure Identified:** Tracked £24,852 across 28 active risk flags.
* **Primary Threat Vector:** Rapid Movement of Funds accounted for over 90% of flagged operational anomalies.
* **Critical Risk Ratio:** Identified critical severity threshold alerts requiring immediate compliance review.

---

## 📂 Project Repository Structure


Dashboard/
│
├── README.md                 # Project documentation and executive summary
├── Viz.pbix                  # Power BI dashboard source file
├── Viz.pdf                   # Exported PDF version of the Power BI dashboard
├── sql.py                    # DuckDB / SQL operational AML rule engine
├── import pandas as pd.py    # Synthetic FinTech data generation script
├── master_fincrime_alerts.csv # Consolidated AML risk alerts dataset
├── users.csv                 # Synthetic user profile & KYC status data
└── transactions.csv          # Synthetic transaction ledger
