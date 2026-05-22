from pathlib import Path
import shutil

import kagglehub


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_OUTPUT = DATA_DIR / "raw_ecommerce.csv"


def locate_csv(download_path: Path) -> Path:
    csv_files = sorted(download_path.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found inside Kaggle download: {download_path}")
    return csv_files[0]


def download_dataset() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    import kagglehub
    path = kagglehub.dataset_download("carrie1/ecommerce-data")

    source_csv = locate_csv(Path(path))
    shutil.copy2(source_csv, RAW_OUTPUT)
    print(f"Dataset downloaded from KaggleHub: {source_csv}")
    print(f"Raw CSV copied to: {RAW_OUTPUT}")
    return RAW_OUTPUT


if __name__ == "__main__":
    download_dataset()
