"""Data loading and analysis helpers (pandas / NumPy). No web code here."""
from pathlib import Path

import numpy as np
import pandas as pd


def load_data(path):
    """Load the Kaggle CSV and clean it (strip names, drop duplicates/NaN, parse dates)."""
    df = pd.read_csv(Path(path))
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates().dropna()
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def summary(df):
    prices = np.array(df["Unit price"], dtype=float)
    ratings = np.array(df["Rating"], dtype=float)
    return {
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "unit_price": {
            "mean": round(float(np.mean(prices)), 2),
            "max": round(float(np.max(prices)), 2),
            "min": round(float(np.min(prices)), 2),
            "std": round(float(np.std(prices)), 2),
        },
        "items_rated_above_8": int(np.sum(ratings > 8.0)),
    }


def sales_by_branch(df):
    s = df.groupby("Branch")["Sales"].sum().round(2)
    return {"totals": s.to_dict(), "top_branch": s.idxmax()}


def rating_by_product_line(df):
    s = df.groupby("Product line")["Rating"].mean().round(2)
    return {"averages": s.to_dict(), "top_product_line": s.idxmax()}


def payment_counts(df):
    s = df["Payment"].value_counts()
    return {"counts": {k: int(v) for k, v in s.items()}, "most_used": s.idxmax()}


def pivot(df):
    p = df.pivot_table(index="Product line", columns="Branch", values="Sales", aggfunc="sum")
    return p.round(2).fillna(0).to_dict(orient="index")


def export_report(df, path):
    """Write the Excel report (clean data + pivot table) and return the path."""
    p = df.pivot_table(index="Product line", columns="Branch", values="Sales", aggfunc="sum")
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name="Clean_Data", index=False)
        p.to_excel(writer, sheet_name="Pivot_tab")
    return path