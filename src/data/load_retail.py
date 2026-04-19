"""
Load raw Online Retail II Excel file into SQLite database.
Saves both sheets (Year 2009-2010 and Year 2010-2011) as a
single unified table: transactions.
"""

import sqlite3
from pathlib import Path

import pandas as pd
from loguru import logger

# paths
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EXCEL_PATH = DATA_DIR / "online_retail_II.xlsx"
DB_PATH = DATA_DIR / "retail.db"


def load_excel_to_df() -> pd.DataFrame:
    """Read both sheets from Excel and combine into one DataFrame."""
    logger.info("Reading Sheet 1 (2009-2010)...")
    df1 = pd.read_excel(EXCEL_PATH, sheet_name="Year 2009-2010", engine="openpyxl")

    logger.info("Reading Sheet 2 (2010-2011)...")
    df2 = pd.read_excel(EXCEL_PATH, sheet_name="Year 2010-2011", engine="openpyxl")

    df = pd.concat([df1, df2], ignore_index=True)
    logger.info(f"Combined shape: {df.shape}")
    return df


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to snake_case."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # Expected columns after rename:
    # invoice, stockcode, description, quantity,
    # invoicedate, price, customer_id, country
    logger.info(f"Columns: {df.columns.tolist()}")
    return df


def save_to_sqlite(df: pd.DataFrame) -> None:
    """Write DataFrame to SQLite table: transactions."""
    logger.info(f"Saving {len(df):,} rows to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()
    logger.success(f"Database saved → {DB_PATH}")


def run_sanity_checks(df: pd.DataFrame) -> None:
    """Print quick sanity stats to confirm data loaded correctly."""
    print("\n── Sanity Checks ──────────────────────────────")
    print(f"  Total rows        : {len(df):,}")
    print(f"  Total columns     : {len(df.columns)}")
    print(
        f"  Date range        : {df['invoicedate'].min()} → {df['invoicedate'].max()}"
    )
    print(f"  Unique customers  : {df['customer_id'].nunique():,}")
    print(f"  Unique products   : {df['stockcode'].nunique():,}")
    print(f"  Unique countries  : {df['country'].nunique():,}")
    print(f"  Missing values    :\n{df.isnull().sum()}")
    print("────────────────────────────────────────────────\n")


def main() -> None:
    logger.info("Starting data ingestion pipeline...")
    df = load_excel_to_df()
    df = standardise_columns(df)
    run_sanity_checks(df)
    save_to_sqlite(df)
    logger.success("Data ingestion complete!")


if __name__ == "__main__":
    main()
