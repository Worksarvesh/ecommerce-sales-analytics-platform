from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_CSV = DATA_DIR / "raw_ecommerce.csv"
CLEAN_CSV = DATA_DIR / "cleaned_ecommerce.csv"

REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]


def validate_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    extra = [column for column in df.columns if column not in REQUIRED_COLUMNS]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    if extra:
        df.drop(columns=extra, inplace=True)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    df = df[REQUIRED_COLUMNS].copy()

    df = df.dropna(subset=["CustomerID"])
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C", na=False)]
    df = df.drop_duplicates()

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    df = df.dropna(subset=["Quantity", "UnitPrice", "CustomerID", "InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["CustomerID"] = df["CustomerID"].astype("int64")
    df["Quantity"] = df["Quantity"].astype("int64")
    df["StockCode"] = df["StockCode"].astype(str).str.strip()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    df = df[
        (df["StockCode"] != "")
        & (df["InvoiceNo"] != "")
        & (df["Description"] != "")
        & (df["Country"] != "")
    ]

    df["TotalRevenue"] = (df["Quantity"] * df["UnitPrice"]).round(2)
    return df.reset_index(drop=True)


def clean_csv(input_path: Path = RAW_CSV, output_path: Path = CLEAN_CSV) -> Path:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {input_path}. Run scripts/download_dataset.py first."
        )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path, encoding="ISO-8859-1")
    cleaned = clean_dataframe(df)
    cleaned.to_csv(output_path, index=False)
    print(f"Cleaned rows: {len(cleaned):,}")
    print(f"Cleaned CSV saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else RAW_CSV
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else CLEAN_CSV
    clean_csv(source, target)
