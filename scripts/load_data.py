from pathlib import Path
import sys

import pandas as pd
from psycopg2.extras import execute_values

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.db_connection import get_db_connection  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_CSV = PROJECT_ROOT / "data" / "cleaned_ecommerce.csv"
SCHEMA_SQL = PROJECT_ROOT / "database.sql"


def run_schema() -> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
        connection.commit()
    print("Database schema created successfully.")


def prepare_tables(df: pd.DataFrame):
    customers = (
        df[["CustomerID", "Country"]]
        .sort_values(["CustomerID", "Country"])
        .drop_duplicates(subset=["CustomerID"], keep="last")
        .rename(columns={"CustomerID": "customer_id", "Country": "country"})
    )

    products = (
        df.sort_values(["StockCode", "InvoiceDate"])
        .groupby("StockCode", as_index=False)
        .agg(
            description=("Description", lambda x: x.mode().iat[0] if not x.mode().empty else x.iloc[-1]),
            unit_price=("UnitPrice", "median"),
        )
        .rename(columns={"StockCode": "stock_code"})
    )
    products["unit_price"] = products["unit_price"].round(2).clip(lower=0.01)

    orders = (
        df.sort_values(["InvoiceNo", "StockCode", "InvoiceDate"])
        .groupby(["InvoiceNo", "StockCode"], as_index=False)
        .agg(
            customer_id=("CustomerID", "first"),
            quantity=("Quantity", "sum"),
            invoice_date=("InvoiceDate", "min"),
            total_revenue=("TotalRevenue", "sum"),
        )
        .rename(columns={"InvoiceNo": "invoice_no", "StockCode": "stock_code"})
    )
    orders["total_revenue"] = orders["total_revenue"].round(2)
    return customers, products, orders


def load_dataframe(df: pd.DataFrame) -> None:
    customers, products, orders = prepare_tables(df)

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            execute_values(
                cursor,
                """
                INSERT INTO customers (customer_id, country)
                VALUES %s
                ON CONFLICT (customer_id) DO UPDATE
                SET country = EXCLUDED.country;
                """,
                list(customers.itertuples(index=False, name=None)),
                page_size=5000,
            )

            execute_values(
                cursor,
                """
                INSERT INTO products (stock_code, description, unit_price)
                VALUES %s
                ON CONFLICT (stock_code) DO UPDATE
                SET description = EXCLUDED.description,
                    unit_price = EXCLUDED.unit_price;
                """,
                list(products.itertuples(index=False, name=None)),
                page_size=5000,
            )

            execute_values(
                cursor,
                """
                INSERT INTO orders (
                    invoice_no, stock_code, customer_id, quantity, invoice_date, total_revenue
                )
                VALUES %s
                ON CONFLICT (invoice_no, stock_code) DO UPDATE
                SET customer_id = EXCLUDED.customer_id,
                    quantity = EXCLUDED.quantity,
                    invoice_date = EXCLUDED.invoice_date,
                    total_revenue = EXCLUDED.total_revenue;
                """,
                list(
                    orders[
                        ["invoice_no", "stock_code", "customer_id", "quantity", "invoice_date", "total_revenue"]
                    ].itertuples(index=False, name=None)
                ),
                page_size=5000,
            )
        connection.commit()

    print(f"Loaded customers: {len(customers):,}")
    print(f"Loaded products: {len(products):,}")
    print(f"Loaded orders: {len(orders):,}")


def load_csv(csv_path: Path = CLEAN_CSV, recreate_schema: bool = True) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}. Run scripts/clean_data.py first.")

    if recreate_schema:
        run_schema()

    df = pd.read_csv(csv_path, parse_dates=["InvoiceDate"])
    load_dataframe(df)


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CLEAN_CSV
    load_csv(path)
