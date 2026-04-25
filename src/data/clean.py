"""
Cleaning pipeline for Online Retail II dataset.
Produces a clean analytical parquet file for downstream ML tasks.

Cleaning steps:
    1. Remove duplicate rows
    2. Separate returns from purchases
    3. Drop rows with missing customer_id
    4. Drop zero/negative price rows
    5. Cap quantity and price outliers (domain-based, not IQR)
    6. Add derived columns: revenue, year_month, is_uk
    7. Save clean dataset to parquet
"""

import sqlite3
import warnings
from pathlib import Path

import pandas as pd
from loguru import logger

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "retail.db"
OUTPUT_PATH = ROOT / "data" / "retail_clean.parquet"


def load_raw(db_path: Path) -> pd.DataFrame:
    """Load raw transactions from SQLite."""
    logger.info("Loading raw transactions from SQLite...")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()

    # Fix types
    df["invoicedate"] = pd.to_datetime(df["invoicedate"])
    df["customer_id"] = df["customer_id"].astype("Int64")

    logger.info(f"Raw shape: {df.shape}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logger.info(f"Duplicates removed: {before - after:,}")
    return df


def separate_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split into purchases and returns.
    Returns have negative quantity OR invoice starting with 'C'.
    """
    is_return = (df["quantity"] < 0) | (df["invoice"].astype(str).str.startswith("C"))
    returns = df[is_return].copy()
    purchases = df[~is_return].copy()
    logger.info(f"Purchases : {len(purchases):,}")
    logger.info(f"Returns   : {len(returns):,}")
    return purchases, returns


def drop_missing_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with no customer_id (guest checkouts)."""
    before = len(df)
    df = df[df["customer_id"].notna()].copy()
    after = len(df)
    logger.info(f"Dropped missing customer_id: {before - after:,}")
    return df


def drop_bad_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with zero or negative price."""
    before = len(df)
    df = df[df["price"] > 0].copy()
    after = len(df)
    logger.info(f"Dropped bad prices: {before - after:,}")
    return df


def cap_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cap extreme outliers using domain-based thresholds.
    We cap rather than drop — real transactions, just extreme.

    Thresholds chosen from domain knowledge:
        quantity : max 10,000 units per line (bulk wholesale max)
        price    : max £5,000 per unit (luxury/custom items)
    """
    qty_cap = 10_000
    price_cap = 5_000

    qty_outliers = (df["quantity"] > qty_cap).sum()
    price_outliers = (df["price"] > price_cap).sum()

    df["quantity"] = df["quantity"].clip(upper=qty_cap)
    df["price"] = df["price"].clip(upper=price_cap)

    logger.info(f"Quantity capped (>{qty_cap})   : {qty_outliers:,} rows")
    logger.info(f"Price capped    (>£{price_cap}): {price_outliers:,} rows")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add useful derived columns for analysis and modelling."""
    df["revenue"] = df["quantity"] * df["price"]
    df["year_month"] = df["invoicedate"].dt.to_period("M").astype(str)
    df["year"] = df["invoicedate"].dt.year
    df["month"] = df["invoicedate"].dt.month
    df["day_of_week"] = df["invoicedate"].dt.dayofweek  # 0=Mon, 6=Sun
    df["hour"] = df["invoicedate"].dt.hour
    df["is_uk"] = (df["country"] == "United Kingdom").astype(int)
    logger.info(
        "Derived columns added: revenue, year_month, year, month, day_of_week, hour, is_uk"
    )
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print final dataset summary."""
    print("\n── Clean Dataset Summary ───────────────────────────")
    print(f"  Rows              : {len(df):,}")
    print(f"  Columns           : {len(df.columns)}")
    print(f"  Unique customers  : {df['customer_id'].nunique():,}")
    print(f"  Unique products   : {df['stockcode'].nunique():,}")
    print(f"  Unique countries  : {df['country'].nunique():,}")
    print(
        f"  Date range        : {df['invoicedate'].min()} → {df['invoicedate'].max()}"
    )
    print(f"  Total revenue     : £{df['revenue'].sum():,.2f}")
    print(f"  Missing values    : {df.isnull().sum().sum()}")
    print("─────────────────────────────────────────────────────\n")


def run_pipeline() -> pd.DataFrame:
    """Run the full cleaning pipeline end-to-end."""
    logger.info("═" * 50)
    logger.info("Starting cleaning pipeline...")
    logger.info("═" * 50)

    df = load_raw(DB_PATH)
    df = remove_duplicates(df)
    df, returns = separate_returns(df)
    df = drop_missing_customers(df)
    df = drop_bad_prices(df)
    df = cap_outliers(df)
    df = add_derived_columns(df)

    print_summary(df)

    # Save clean dataset
    df.to_parquet(OUTPUT_PATH, index=False)
    logger.success(f"Clean dataset saved → {OUTPUT_PATH}")

    # Save returns separately (useful for future analysis)
    returns_path = ROOT / "data" / "retail_returns.parquet"
    returns.to_parquet(returns_path, index=False)
    logger.success(f"Returns dataset saved → {returns_path}")

    return df


if __name__ == "__main__":
    run_pipeline()
