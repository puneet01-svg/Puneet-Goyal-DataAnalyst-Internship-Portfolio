# Task 2 — SQL & Data Extraction (9-Day Plan)

Complete implementation of the Day 9-17 plan: SQL fundamentals → advanced SQL
→ Python + SQL integration. Everything here was executed and verified to run
end-to-end (see `notebook/Task2_SQL_Python_Integration.ipynb` for full output).

## What's inside

```
project/
├── data/
│   ├── generate_data.py         # builds the sample dataset from scratch
│   ├── validate_queries.py      # sanity-checks every query in sql/queries.sql
│   ├── shop.db                  # the SQLite database (400 customers, 3,500 orders, 6,644 line items)
│   └── monthly_sales_trend.csv  # example exported query result
├── sql/
│   └── queries.sql              # every required SQL topic, organized by day
├── db_utils.py                  # reusable connection module (SQLite + PostgreSQL-ready)
├── scripts/
│   └── run_queries.py           # standalone script: connect, parameterized query, pandas.read_sql()
└── notebook/
    └── Task2_SQL_Python_Integration.ipynb   # Day 15-17 notebook, fully executed
```

## Dataset

Since the task assumes a "cleaned dataset" to import, `generate_data.py`
creates one: a realistic e-commerce schema —
`customers`, `categories`, `products`, `orders`, `order_items` — spanning
Jan 2025 to Jun 2026, with 400 customers, 31 products across 6 categories,
3,500 orders, and 6,644 order line items. Re-run it any time to regenerate
`shop.db` from scratch.

## Day 9-11: SQL Fundamentals (`sql/queries.sql`, Part 1)
- SELECT / WHERE / ORDER BY / LIMIT
- JOINs: INNER, LEFT, RIGHT, FULL
- GROUP BY, HAVING, COUNT/SUM/AVG/MIN/MAX
- Subqueries (correlated + non-correlated) and CTEs (`WITH`)
- Window functions: ROW_NUMBER, RANK, LAG, LEAD

## Day 12-14: Advanced SQL (`sql/queries.sql`, Part 2)
- Monthly sales trend
- Top 10 customers by revenue
- Customer retention rate (month-over-month cohort logic)
- Product category performance (with % of total revenue)
- 7-day moving average and cumulative revenue (window functions)
- Two views: `vw_customer_ltv`, `vw_monthly_category_revenue`
- `EXPLAIN QUERY PLAN` before/after adding indexes on the key filter/join columns

## Day 15-17: Python + SQL Integration
- `db_utils.py`: one module, two backends — SQLite by default, or PostgreSQL
  via `DB_BACKEND=postgres` + `DB_URL` (built on SQLAlchemy so the rest of
  the code doesn't care which backend is active; psycopg2 is the driver
  behind the Postgres URL)
- `scripts/run_queries.py`: connects, runs a plain query, a parameterized
  query, and a business query, then exports a CSV
- `notebook/Task2_SQL_Python_Integration.ipynb`: executes SQL directly from
  the notebook, loads results with `pandas.read_sql()`, charts the monthly
  trend and category revenue, and demonstrates parameterized queries

## Running it yourself

```bash
pip install sqlalchemy pandas matplotlib

# (re)build the database
python data/generate_data.py

# validate every query in queries.sql runs cleanly
python data/validate_queries.py

# run the standalone integration script
python scripts/run_queries.py

# open the notebook
jupyter lab notebook/Task2_SQL_Python_Integration.ipynb
```

To point at PostgreSQL instead of SQLite:
```bash
export DB_BACKEND=postgres
export DB_URL="postgresql+psycopg2://user:pass@localhost:5432/shopdb"
```

## Suggested LinkedIn post

> Task 2: SQL mastery complete! Wrote 20+ complex queries for business
> insights — monthly trends, retention, category performance, moving
> averages — and integrated Python with SQLite/PostgreSQL for automated
> data extraction using SQLAlchemy and pandas. #SQL #DataExtraction
