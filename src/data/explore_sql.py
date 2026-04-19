"""
5 exploratory SQL queries on the retail database.
Run this to understand the data before EDA notebooks.
"""

import sqlite3
from pathlib import Path

from loguru import logger

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "retail.db"


def run_query(conn: sqlite3.Connection, title: str, sql: str) -> None:
    """Run a query and pretty-print results."""
    import pandas as pd

    print(f"\n{'═' * 55}")
    print(f"  {title}")
    print(f"{'═' * 55}")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))


def main() -> None:
    conn = sqlite3.connect(DB_PATH)

    # ── Query 1: Top 10 countries by total revenue ──────────────
    run_query(
        conn,
        "Q1 — Top 10 Countries by Revenue",
        """
        SELECT
            country,
            COUNT(DISTINCT invoice)            AS total_orders,
            ROUND(SUM(quantity * price), 2)    AS total_revenue,
            ROUND(AVG(quantity * price), 2)    AS avg_order_value
        FROM transactions
        WHERE quantity > 0
          AND price > 0
        GROUP BY country
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    )

    # ── Query 2: Monthly revenue trend ──────────────────────────
    run_query(
        conn,
        "Q2 — Monthly Revenue Trend",
        """
        SELECT
            SUBSTR(invoicedate, 1, 7)           AS month,
            COUNT(DISTINCT invoice)             AS orders,
            ROUND(SUM(quantity * price), 2)     AS revenue
        FROM transactions
        WHERE quantity > 0
          AND price > 0
        GROUP BY month
        ORDER BY month;
    """,
    )

    # ── Query 3: Top 10 best-selling products ───────────────────
    run_query(
        conn,
        "Q3 — Top 10 Best-Selling Products",
        """
        SELECT
            stockcode,
            description,
            SUM(quantity)                       AS units_sold,
            ROUND(SUM(quantity * price), 2)     AS revenue
        FROM transactions
        WHERE quantity > 0
          AND price > 0
          AND description IS NOT NULL
        GROUP BY stockcode, description
        ORDER BY units_sold DESC
        LIMIT 10;
    """,
    )

    # ── Query 4: Return rate by country (negative quantities) ───
    run_query(
        conn,
        "Q4 — Top 10 Countries by Return Rate",
        """
        SELECT
            country,
            SUM(CASE WHEN quantity > 0 THEN 1 ELSE 0 END)  AS purchases,
            SUM(CASE WHEN quantity < 0 THEN 1 ELSE 0 END)  AS returns,
            ROUND(
                100.0 * SUM(CASE WHEN quantity < 0 THEN 1 ELSE 0 END)
                / COUNT(*), 2
            )                                               AS return_rate_pct
        FROM transactions
        GROUP BY country
        HAVING purchases > 100
        ORDER BY return_rate_pct DESC
        LIMIT 10;
    """,
    )

    # ── Query 5: Customer purchase frequency segments ───────────
    run_query(
        conn,
        "Q5 — Customer Purchase Frequency Breakdown",
        """
        SELECT
            CASE
                WHEN order_count = 1        THEN '1 — One-time buyer'
                WHEN order_count BETWEEN 2
                     AND 5                  THEN '2 — Occasional (2-5)'
                WHEN order_count BETWEEN 6
                     AND 20                 THEN '3 — Regular (6-20)'
                ELSE                             '4 — VIP (20+)'
            END                             AS segment,
            COUNT(*)                        AS customer_count,
            ROUND(AVG(order_count), 1)      AS avg_orders
        FROM (
            SELECT
                customer_id,
                COUNT(DISTINCT invoice)     AS order_count
            FROM transactions
            WHERE customer_id IS NOT NULL
              AND quantity > 0
            GROUP BY customer_id
        )
        GROUP BY segment
        ORDER BY segment;
    """,
    )

    conn.close()
    logger.success("All queries complete!")


if __name__ == "__main__":
    main()
