"""
db_utils.py
-----------
Reusable database connection module for Task 2 (Day 15-17: Python + SQL
Integration).

Supports two backends so the same module works whether you're running
locally against SQLite (zero setup) or against a PostgreSQL instance
(e.g. via Docker), as called for in the task brief:

    - SQLite    via the standard library `sqlite3` module (used for
                connection pooling underneath SQLAlchemy)
    - PostgreSQL via `psycopg2`

Both paths are wrapped behind SQLAlchemy so the rest of the codebase
(scripts, notebook) can stay backend-agnostic and just call:

    from db_utils import get_engine, run_query, run_parametrized

Usage
-----
    from db_utils import get_engine, run_query

    engine = get_engine()                      # defaults to local SQLite
    df = run_query(engine, "SELECT * FROM customers LIMIT 5")

To point at PostgreSQL instead, set an environment variable before
importing, or pass backend="postgres" explicitly:

    export DB_BACKEND=postgres
    export DB_URL="postgresql+psycopg2://user:pass@localhost:5432/shopdb"
"""

from __future__ import annotations

import os
import contextlib
from pathlib import Path
from typing import Any, Iterable, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DEFAULT_SQLITE_PATH = Path(__file__).parent / "data" / "shop.db"


def get_engine(backend: Optional[str] = None, db_url: Optional[str] = None) -> Engine:
    """
    Build and return a SQLAlchemy Engine.

    Parameters
    ----------
    backend : "sqlite" | "postgres" | None
        Which backend to connect to. Falls back to the DB_BACKEND
        environment variable, then defaults to "sqlite".
    db_url : str | None
        Full SQLAlchemy connection URL. If omitted, a sensible default
        is built for the chosen backend (local shop.db for sqlite, or
        the DB_URL environment variable for postgres).

    Returns
    -------
    sqlalchemy.engine.Engine
    """
    backend = backend or os.getenv("DB_BACKEND", "sqlite")

    if backend == "sqlite":
        url = db_url or f"sqlite:///{DEFAULT_SQLITE_PATH}"
        # check_same_thread=False lets the same connection be reused
        # safely across a Jupyter kernel's cells / callbacks.
        engine = create_engine(url, connect_args={"check_same_thread": False})

    elif backend == "postgres":
        url = db_url or os.getenv(
            "DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/shopdb"
        )
        engine = create_engine(url)

    else:
        raise ValueError(f"Unknown backend '{backend}'. Use 'sqlite' or 'postgres'.")

    return engine


@contextlib.contextmanager
def get_connection(engine: Optional[Engine] = None):
    """Context-managed connection: `with get_connection() as conn: ...`"""
    engine = engine or get_engine()
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def run_query(engine: Optional[Engine], sql: str) -> pd.DataFrame:
    """
    Execute a read-only SQL query and return the result as a DataFrame.
    Thin wrapper around pandas.read_sql() as required by the task brief.
    """
    engine = engine or get_engine()
    return pd.read_sql(text(sql), engine)


def run_parametrized(engine: Optional[Engine], sql: str, params: dict[str, Any]) -> pd.DataFrame:
    """
    Execute a parameterized query safely (protects against SQL injection).

    Example
    -------
        run_parametrized(
            engine,
            "SELECT * FROM customers WHERE city = :city AND customer_id > :min_id",
            {"city": "Delhi", "min_id": 10},
        )
    """
    engine = engine or get_engine()
    return pd.read_sql(text(sql), engine, params=params)


def execute_statement(engine: Optional[Engine], sql: str, params: Optional[dict] = None) -> None:
    """
    Execute a non-SELECT statement (INSERT/UPDATE/DELETE/DDL) safely with
    parameter binding, committing the transaction.
    """
    engine = engine or get_engine()
    with engine.begin() as conn:  # begin() auto-commits on success, rolls back on error
        conn.execute(text(sql), params or {})


def run_many_parametrized(engine: Optional[Engine], sql: str, param_list: Iterable[dict]) -> None:
    """
    Execute the same parameterized statement for many rows in one
    transaction (e.g. bulk inserts), avoiding SQL injection and avoiding
    one round trip per row.
    """
    engine = engine or get_engine()
    with engine.begin() as conn:
        for params in param_list:
            conn.execute(text(sql), params)


if __name__ == "__main__":
    # Quick self-test when run directly: `python db_utils.py`
    engine = get_engine()
    df = run_query(engine, "SELECT COUNT(*) AS n_customers FROM customers")
    print("Connected OK. customers table row count:")
    print(df)
