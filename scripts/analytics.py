from decimal import Decimal
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.db_connection import get_sqlalchemy_engine  # noqa: E402


def _serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def dataframe_to_records(df: pd.DataFrame):
    return [
        {column: _serialize_value(value) for column, value in row.items()}
        for row in df.to_dict(orient="records")
    ]


def fetch_dataframe(query: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_sqlalchemy_engine()
    with engine.connect() as connection:
        return pd.read_sql_query(text(query), connection, params=params)


def get_total_sales() -> dict:
    df = fetch_dataframe("SELECT COALESCE(SUM(total_revenue), 0) AS total_revenue FROM orders;")
    return {"total_revenue": float(df.iloc[0]["total_revenue"])}


def get_monthly_sales() -> list[dict]:
    df = fetch_dataframe(
        """
        SELECT
            DATE_TRUNC('month', invoice_date) AS month,
            SUM(total_revenue) AS revenue
        FROM orders
        GROUP BY month
        ORDER BY month;
        """
    )
    df["month"] = pd.to_datetime(df["month"]).dt.strftime("%Y-%m")
    return dataframe_to_records(df)


def get_top_products(limit: int = 10) -> list[dict]:
    return dataframe_to_records(
        fetch_dataframe(
            """
            SELECT
                p.description,
                SUM(o.quantity) AS total_sold
            FROM orders o
            JOIN products p
            ON o.stock_code = p.stock_code
            GROUP BY p.description
            ORDER BY total_sold DESC
            LIMIT :limit;
            """,
            {"limit": limit},
        )
    )


def get_country_sales() -> list[dict]:
    return dataframe_to_records(
        fetch_dataframe(
            """
            SELECT
                c.country,
                SUM(o.total_revenue) AS revenue
            FROM orders o
            JOIN customers c
            ON o.customer_id = c.customer_id
            GROUP BY c.country
            ORDER BY revenue DESC;
            """
        )
    )


def get_best_customers(limit: int = 10) -> list[dict]:
    return dataframe_to_records(
        fetch_dataframe(
            """
            SELECT
                customer_id,
                SUM(total_revenue) AS revenue
            FROM orders
            GROUP BY customer_id
            ORDER BY revenue DESC
            LIMIT :limit;
            """,
            {"limit": limit},
        )
    )


def get_average_order_value() -> dict:
    df = fetch_dataframe(
        """
        SELECT COALESCE(AVG(order_total), 0) AS average_order_value
        FROM (
            SELECT invoice_no, SUM(total_revenue) AS order_total
            FROM orders
            GROUP BY invoice_no
        ) x;
        """
    )
    return {"average_order_value": float(df.iloc[0]["average_order_value"])}


def get_customer_ranking(limit: int | None = None) -> list[dict]:
    query = """
        SELECT
            customer_id,
            SUM(total_revenue) AS revenue,
            RANK() OVER (ORDER BY SUM(total_revenue) DESC) AS rank
        FROM orders
        GROUP BY customer_id
        ORDER BY rank
    """
    params = {}
    if limit:
        query += " LIMIT :limit"
        params["limit"] = limit
    query += ";"
    return dataframe_to_records(fetch_dataframe(query, params))


def export_powerbi_dataframe() -> pd.DataFrame:
    return fetch_dataframe(
        """
        SELECT
            o.invoice_no,
            o.customer_id,
            c.country,
            o.stock_code,
            p.description,
            p.unit_price,
            o.quantity,
            o.invoice_date,
            o.total_revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.stock_code = p.stock_code
        ORDER BY o.invoice_date, o.invoice_no, o.stock_code;
        """
    )
