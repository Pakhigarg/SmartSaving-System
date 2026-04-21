"""
feature_engineering.py — Feature Engineering for Budget Buddy
Transforms raw columns into meaningful ML-ready features.
 
New features created:
  ┌──────────────────────┬──────────────────────────────────────────────────┐
  │ Feature              │ Meaning                                          │
  ├──────────────────────┼──────────────────────────────────────────────────┤
  │ expense_ratio        │ amount / income  → how much of income is spent   │
  │ savings_rate         │ savings / income → financial health score        │
  │ food_ratio           │ food / income                                    │
  │ transport_ratio      │ transport / income                               │
  │ shopping_ratio       │ shopping / income                                │
  │ budget_utilization   │ amount / budget  → over/under budget indicator   │
  │ is_weekend           │ 1 if Weekend, else 0                             │
  │ month                │ calendar month (1-12)                            │
  │ quarter              │ fiscal quarter (1-4)                             │
  │ avg_transaction      │ amount per row (proxy for spend habit)           │
  │ category_encoded     │ LabelEncoded category                            │
  │ payment_encoded      │ LabelEncoded payment_method                      │
  └──────────────────────┴──────────────────────────────────────────────────┘
"""
 
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Optional, Tuple
import os, sys, joblib
 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATASET_PATH, MODEL_DIR, REGRESSION_FEATURES, CLUSTER_FEATURES
 
 
# ─── Helpers ──────────────────────────────────────────────────────────────────
def _safe_divide(numerator: pd.Series, denominator: pd.Series,
                 fill: float = 0.0) -> pd.Series:
    """Division that replaces inf/nan with fill value."""
    result = numerator / denominator.replace(0, np.nan)
    return result.fillna(fill).replace([np.inf, -np.inf], fill)
 
 
# ─── Main engineering function ────────────────────────────────────────────────
def engineer_features(df: pd.DataFrame,
                       fit_encoders: bool = True,
                       encoders: Optional[dict] = None) -> Tuple[pd.DataFrame, dict]:
    """
    Adds engineered features to df.
 
    Parameters
    ----------
    df           : raw or partially-processed DataFrame
    fit_encoders : True  → fit new LabelEncoders (training time)
                   False → use existing encoders from `encoders` dict (inference)
    encoders     : dict with keys 'category' and 'payment' when fit_encoders=False
 
    Returns
    -------
    df       : DataFrame with new columns appended
    encoders : dict {'category': LabelEncoder, 'payment': LabelEncoder}
    """
    df = df.copy()
 
    # ── 1. Parse dates ────────────────────────────────────────────────────────
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])
 
    df["month"]   = df["date"].dt.month          # 1–12
    df["quarter"] = df["date"].dt.quarter        # 1–4
 
    # ── 2. Binary flag ────────────────────────────────────────────────────────
    df["is_weekend"] = (df["day_type"] == "Weekend").astype(int)
 
    # ── 3. Ratio features ─────────────────────────────────────────────────────
    df["expense_ratio"]      = _safe_divide(df["amount"],    df["income"])
    df["savings_rate"]       = _safe_divide(df["savings"],   df["income"])
    df["food_ratio"]         = _safe_divide(df["food"],      df["income"])
    df["transport_ratio"]    = _safe_divide(df["transport"], df["income"])
    df["shopping_ratio"]     = _safe_divide(df["shopping"],  df["income"])
    df["budget_utilization"] = _safe_divide(df["amount"],    df["budget"])
 
    # ── 4. Average transaction (groupby category per row as proxy) ────────────
    # mean amount per category — captures typical spend per category
    cat_avg = df.groupby("category")["amount"].transform("mean")
    df["avg_transaction"] = cat_avg
 
    # ── 5. Label-encode categorical columns ───────────────────────────────────
    if fit_encoders:
        encoders = {}
        for col, key in [("category", "category"), ("payment_method", "payment")]:
            le = LabelEncoder()
            df[f"{key}_encoded"] = le.fit_transform(df[col])
            encoders[key] = le
    else:
        # inference time: use existing encoders, handle unseen labels gracefully
        assert encoders is not None, "Pass encoders dict when fit_encoders=False"
        for col, key in [("category", "category"), ("payment_method", "payment")]:
            le: LabelEncoder = encoders[key]
            # Map unseen labels to the most-frequent class (index 0 after sort)
            df[f"{key}_encoded"] = df[col].apply(
                lambda x: le.transform([x])[0]
                if x in le.classes_ else 0
            )
 
    print(f"  [✓] Feature engineering complete — {len(df.columns)} columns total")
    return df, encoders
 
 
# ─── Select feature matrices ──────────────────────────────────────────────────
def get_regression_Xy(df: pd.DataFrame):
    """Return (X, y) ready for regression training."""
    X = df[REGRESSION_FEATURES].values
    y = df["amount"].values
    return X, y
 
 
def get_cluster_X(df: pd.DataFrame):
    """Return X ready for clustering."""
    return df[CLUSTER_FEATURES].values
 
 
# ─── Save / load encoders ─────────────────────────────────────────────────────
def save_encoders(encoders: dict, path: str = None):
    if path is None:
        path = os.path.join(MODEL_DIR, "encoders.joblib")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(encoders, path)
    print(f"  [✓] Encoders saved → {path}")
 
 
def load_encoders(path: str = None) -> dict:
    if path is None:
        path = os.path.join(MODEL_DIR, "encoders.joblib")
    return joblib.load(path)
 
 
# ─── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df_raw = pd.read_csv(DATASET_PATH)
    df_eng, enc = engineer_features(df_raw, fit_encoders=True)
    print(df_eng[REGRESSION_FEATURES].head(3).to_string())
    print("\nCluster features sample:")
    print(df_eng[CLUSTER_FEATURES].head(3).to_string())
 
