"""
run_queries.py
--------------
Demonstrates Day 15-17 requirements outside of Jupyter:
    - Connect Python to the database via db_utils (SQLAlchemy)
    - Load query results into pandas DataFrames with pandas.read_sql()
    - Use parameterized queries to avoid SQL injection
    - Reuse the db_utils.py connection module

Run with:  python scripts/run_queries.py
"""

import sys
from pathlib import Path

# Make db_utils importable when running this script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db_utils import get_engine, run_query, run_parametrized  # noqa: E402


def main():
    engine = get_engine()  # local SQLite by default

    print("=" * 70)
    print("1) Basic query -> DataFrame via pandas.read_sql()")
    print("=" * 70)
    df_top_categories = run_query(engine, """
        SELECT cat.category_name,
               ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM categories cat
        JOIN products p     ON p.category_id = cat.category_id
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY cat.category_name
        ORDER BY revenue DESC
    """)
    print(df_top_categories.to_string(index=False))

    print("\n" + "=" * 70)
    print("2) Parameterized query (safe from SQL injection)")
    print("=" * 70)
    # Even if `city` came from untrusted user input, binding via :city
    # means it can never break out of the string literal context.
    city = "Delhi"
    min_spend = 10000
    df_city_customers = run_parametrized(
        engine,
        """
        SELECT c.full_name, c.city, SUM(o.order_total) AS total_spend
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        WHERE c.city = :city
          AND o.status = 'completed'
        GROUP BY c.full_name, c.city
        HAVING SUM(o.order_total) > :min_spend
        ORDER BY total_spend DESC
        """,
        {"city": city, "min_spend": min_spend},
    )
    print(f"Customers in {city} with completed spend > {min_spend}:")
    print(df_city_customers.to_string(index=False))

    print("\n" + "=" * 70)
    print("3) Monthly sales trend -> DataFrame, ready for plotting/export")
    print("=" * 70)
    df_monthly = run_query(engine, """
        SELECT strftime('%Y-%m', order_date) AS month,
               COUNT(*) AS orders_count,
               ROUND(SUM(order_total), 2) AS monthly_revenue
        FROM orders
        WHERE status = 'completed'
        GROUP BY month
        ORDER BY month
    """)
    print(df_monthly.to_string(index=False))

    # Example of writing a result back out for downstream use
    out_path = Path(__file__).resolve().parent.parent / "data" / "monthly_sales_trend.csv"
    df_monthly.to_csv(out_path, index=False)
    print(f"\nSaved monthly sales trend to: {out_path}")


if __name__ == "__main__":
    main()
