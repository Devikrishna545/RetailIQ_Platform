"""
RFM feature engineering + customer segmentation.
Reusable module — called by notebooks and the API.
"""

from datetime import timedelta

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Compute RFM features from clean transaction data."""
    reference_date = df["invoicedate"].max() + timedelta(days=1)

    rfm = (
        df.groupby("customer_id")
        .agg(
            recency=("invoicedate", lambda x: (reference_date - x.max()).days),
            frequency=("invoice", "nunique"),
            monetary=("revenue", "sum"),
            avg_order_value=("revenue", "mean"),
            unique_products=("stockcode", "nunique"),
            tenure_days=("invoicedate", lambda x: (x.max() - x.min()).days),
            is_uk=("is_uk", "first"),
        )
        .reset_index()
    )
    logger.info(f"RFM computed for {len(rfm):,} customers")
    return rfm


def segment_customers(rfm: pd.DataFrame, k: int = 4) -> pd.DataFrame:
    """Run K-Means segmentation on RFM features."""
    rfm["monetary_log"] = np.log1p(rfm["monetary"])
    rfm["frequency_log"] = np.log1p(rfm["frequency"])

    features = ["recency", "frequency_log", "monetary_log"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(rfm[features])

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    rfm["cluster"] = km.fit_predict(X_scaled)

    # Name by monetary rank
    cluster_rank = (
        rfm.groupby("cluster")["monetary"]
        .mean()
        .sort_values(ascending=False)
        .index.tolist()
    )
    name_map = {
        cluster_rank[0]: "VIP Champions",
        cluster_rank[1]: "Loyal Regulars",
        cluster_rank[2]: "Churned / Lost",
        cluster_rank[3]: "New / One-timers",
    }
    rfm["segment_name"] = rfm["cluster"].map(name_map)

    logger.info(f"Segments assigned:\n{rfm['segment_name'].value_counts().to_string()}")
    return rfm
