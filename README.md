# 🛒 Olist Brazilian E-Commerce — Batch ETL Pipeline

> A production-style batch ETL pipeline that transforms raw e-commerce data into a query-ready analytical warehouse — built with **Polars**, **PostgreSQL**, and **SQLAlchemy**.

---

## 📌 Overview

This project simulates a **real-world batch ETL workflow** used by data engineering teams to move raw operational data into an analytics-ready warehouse. It uses the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — ~100K real orders across 9 relational tables — and processes it through a clean, three-layer architecture:

```
Raw CSVs  →  Staging Layer  →  Transform (Polars)  →  Warehouse (Star Schema)
```

The result: a PostgreSQL data warehouse ready for BI tools, ad-hoc SQL analysis, or dashboarding.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌───────────────┐
│  Raw CSVs   │ ──▶ │   Staging    │ ──▶ │   Transform     │ ──▶ │   Warehouse   │
│ (data/raw)  │     │  (Postgres)  │     │  (Polars logic) │     │ (Star Schema) │
└─────────────┘     └──────────────┘     └────────────────┘     └───────────────┘
   9 CSV files        Raw, 1:1 mirror       Clean, joined,         Fact + Dim
                       of source data        deduplicated          tables
```

**Why this design?**
- **Staging** preserves raw data exactly as received — critical for auditability and reprocessing without re-reading source files.
- **Transform** applies all business logic in Polars (fast, memory-efficient DataFrame engine).
- **Warehouse** follows a **star schema** — the industry standard for analytical querying — optimized for fast aggregations and joins.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Extraction & Transformation | **Polars** |
| Database | **PostgreSQL** |
| DB Connectivity | **SQLAlchemy** + **psycopg2** |
| Config Management | **python-dotenv** |
| Orchestration | Custom Python (`main.py`) |
| Logging | Python `logging` (file + console) |

---

## 📂 Project Structure

```
olist-etl-pipeline/
│
├── sql/
│   ├── staging/
│   │   └── create_staging_tables.sql      # Raw table DDL
│   └── warehouse/
│       └── create_warehouse_tables.sql    # Star schema DDL
│
├── data/
│   └── raw/                                # Source CSVs (gitignored)
│
├── src/
│   ├── config.py                           # Paths, env vars, DB connection string
│   ├── extract.py                          # Reads raw CSVs into Polars DataFrames
│   ├── transform.py                        # Builds fact/dim tables from staging data
│   └── load.py                             # Loads data into staging + warehouse
│
├── logs/
│   └── etl.log                             # Pipeline execution logs
│
├── main.py                                 # Single orchestrator entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⭐ Data Model — Star Schema

**Grain:** `fact_orders` → one row per order item

| Table | Type | Description |
|---|---|---|
| `fact_orders` | Fact | Order-level metrics — price, freight, payment value, review score |
| `dim_customers` | Dimension | Customer identity, city, state |
| `dim_sellers` | Dimension | Seller identity, city, state |
| `dim_products` | Dimension | Product category (translated to English), dimensions, weight |
| `dim_date` | Dimension | Calendar attributes — year, month, day, weekday |

```
                    ┌────────────────┐
                    │  dim_customers │
                    └───────┬────────┘
                            │
┌───────────────┐   ┌───────▼────────┐   ┌────────────────┐
│  dim_products  │◀──│  fact_orders   │──▶│  dim_sellers   │
└───────────────┘   └───────┬────────┘   └────────────────┘
                            │
                    ┌───────▼────────┐
                    │    dim_date    │
                    └────────────────┘
```

---

## ⚙️ How to Run

**1. Clone & set up environment**
```bash
git clone <your-repo-url>
cd olist-etl-pipeline
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**2. Configure database credentials**
```bash
cp .env.example .env           # then fill in your actual DB password
```

**3. Create the database & schemas**
```sql
CREATE DATABASE olist_db;
CREATE SCHEMA staging;
CREATE SCHEMA warehouse;
```

**4. Create tables**
```bash
psql -U postgres -d olist_db -f sql/staging/create_staging_tables.sql
psql -U postgres -d olist_db -f sql/warehouse/create_warehouse_tables.sql
```

**5. Add the dataset**

Download the [Olist dataset from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place all 9 CSVs into `data/raw/`.

**6. Run the pipeline**
```bash
python main.py
```

This runs the full flow: **Extract → Load Staging → Transform → Load Warehouse**, with logs streamed to both the console and `logs/etl.log`.

---

## 🔑 Key Engineering Decisions

- **Staging/warehouse separation** — keeps raw and modeled data independently auditable, a pattern used across real data platforms.
- **Truncate-and-reload strategy** — refreshes warehouse data on every run while preserving table structure and foreign key constraints (rather than a destructive drop/recreate).
- **Centralized orchestration** — `main.py` is the single source of truth for pipeline execution order and logging configuration.
- **Structured logging** — every run is timestamped and persisted to `logs/etl.log` for traceability and debugging.

---

## 📊 Sample Insight

Querying `fact_orders` joined with `dim_customers` for revenue by state surfaces a clear geographic concentration:

| State | Total Revenue (R$) |
|---|---|
| SP | 5,202,955.05 |
| RJ | 1,824,092.67 |
| MG | 1,585,308.03 |
| RS | 750,304.02 |
| PR | 683,083.76 |

São Paulo alone accounts for the largest share of revenue — consistent with its role as Brazil's primary economic and logistics hub.

---

## 🚀 Possible Future Enhancements

- Incremental loading (only process new/changed records instead of full reload)
- Orchestration with **Apache Airflow**
- Data quality checks with **Great Expectations**
- Containerization with **Docker**
- BI dashboard layer (Metabase / Power BI) on top of the warehouse

---

## 👤 Author

Built as a hands-on data engineering project to practice batch ETL design, dimensional modeling, and pipeline orchestration end-to-end.
