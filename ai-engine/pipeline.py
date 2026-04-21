"""
pipeline.py — Data Pipeline for Budget Buddy
Ties together: load → clean → feature engineer → split → scale.

Design principle: every step is a small, testable function.
The build_pipeline() function chains them all for training.
For inference, use pipeline_for_inference() instead.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Optional
import joblib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (DATASET_PATH, MODEL_DIR, SCALER_PATH, CLUSTER_SCALER_PATH,
                    REGRESSION_FEATURES, CLUSTER_FEATURES, RANDOM_STATE)
from feature_engineering import (engineer_features, get_regression_Xy,
                                  get_cluster_X, save_encoders)


# ─── Step 1: Load ─────────────────────────────────────────────────────────────
def load_data(path: str = DATASET_PATH) -> pd.DataFrame:
    """Load CSV from disk. Returns raw DataFrame."""
    df = pd.read_csv(path, parse_dates=["date"])
    print(f"  [✓] Loaded {len(df):,} rows from {os.path.basename(path)}")
    return df


# ─── Step 2: Validate (sanity checks) ────────────────────────────────────────
def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assert no nulls, no negative income/amounts.
    In production you'd log & route bad rows instead of raising.
    """
    assert df.isnull().sum().sum() == 0, "Dataset contains null values!"
    assert (df["income"] >= 0).all(),    "Negative income detected!"
    assert (df["amount"] >= 0).all(),    "Negative expense amount detected!"
    print(f"  [✓] Validation passed — {len(df):,} clean rows")
    return df


# ─── Step 3: Feature engineering ─────────────────────────────────────────────
def transform(df: pd.DataFrame,
              fit_encoders: bool = True,
              encoders: Optional[dict] = None):
    """Wrapper around feature_engineering.engineer_features."""
    df_eng, encoders = engineer_features(df,
                                         fit_encoders=fit_encoders,
                                         encoders=encoders)
    return df_eng, encoders


# ─── Step 4: Train/test split ─────────────────────────────────────────────────
def split_data(X, y, test_size: float = 0.2):
    """Standard 80/20 stratified-ish random split."""
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE
    )
    print(f"  [✓] Split → train: {len(X_tr):,} | test: {len(X_te):,}")
    return X_tr, X_te, y_tr, y_te


# ─── Step 5: Scale ────────────────────────────────────────────────────────────
def scale_features(X_train, X_test, scaler_path: str = SCALER_PATH):
    """Fit StandardScaler on train, transform both sets. Save scaler."""
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(scaler, scaler_path)
    print(f"  [✓] Scaler fitted & saved → {scaler_path}")
    return X_train_s, X_test_s, scaler


def scale_cluster_features(X, scaler_path: str = CLUSTER_SCALER_PATH):
    """Fit & save a separate scaler for clustering (no y involved)."""
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(scaler, scaler_path)
    print(f"  [✓] Cluster scaler fitted & saved → {scaler_path}")
    return X_s, scaler


# ─── Full training pipeline ───────────────────────────────────────────────────
def build_pipeline(path: str = DATASET_PATH) -> dict:
    """
    Runs the full data pipeline for training.

    Returns a dict with everything models need:
      {
        'df'          : engineered DataFrame,
        'X_train'     : scaled train features (regression),
        'X_test'      : scaled test features  (regression),
        'y_train'     : train labels,
        'y_test'      : test labels,
        'X_cluster'   : scaled features for clustering (full dataset),
        'encoders'    : fitted LabelEncoders,
        'scaler'      : fitted StandardScaler (regression),
        'c_scaler'    : fitted StandardScaler (clustering),
      }
    """
    print("\n🔧  Building data pipeline …")

    df = load_data(path)
    df = validate_data(df)
    df, encoders = transform(df, fit_encoders=True)

    # ── Regression split & scale ──────────────────────────────────────────────
    X_reg, y_reg          = df[REGRESSION_FEATURES].values, df["amount"].values
    X_tr, X_te, y_tr, y_te = split_data(X_reg, y_reg)
    X_tr_s, X_te_s, scaler = scale_features(X_tr, X_te)

    # ── Clustering (full dataset) ─────────────────────────────────────────────
    X_clust              = df[CLUSTER_FEATURES].values
    X_clust_s, c_scaler  = scale_cluster_features(X_clust)

    # ── Persist encoders ──────────────────────────────────────────────────────
    save_encoders(encoders)

    print("✅  Pipeline complete\n")
    return {
        "df":        df,
        "X_train":   X_tr_s,
        "X_test":    X_te_s,
        "y_train":   y_tr,
        "y_test":    y_te,
        "X_cluster": X_clust_s,
        "encoders":  encoders,
        "scaler":    scaler,
        "c_scaler":  c_scaler,
    }


# ─── Inference pipeline (single row dict → scaled array) ─────────────────────
def pipeline_for_inference(row: dict, encoders: dict, scaler, c_scaler) -> dict:
    """
    Convert a single user input dict into ready-to-predict arrays.

    Parameters
    ----------
    row      : dict matching raw CSV column names
    encoders : loaded from encoders.joblib
    scaler   : loaded from scaler.joblib   (regression)
    c_scaler : loaded from cluster_scaler.joblib

    Returns
    -------
    dict with 'X_reg' and 'X_clust' as (1, n_features) arrays
    """
    df_row = pd.DataFrame([row])
    df_row, _ = engineer_features(df_row, fit_encoders=False, encoders=encoders)

    X_reg   = df_row[REGRESSION_FEATURES].values
    X_clust = df_row[CLUSTER_FEATURES].values

    X_reg_s   = scaler.transform(X_reg)
    X_clust_s = c_scaler.transform(X_clust)

    return {"X_reg": X_reg_s, "X_clust": X_clust_s}


# ─── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = build_pipeline()
    print("Keys returned:", list(result.keys()))
    print("X_train shape:", result["X_train"].shape)
    print("X_cluster shape:", result["X_cluster"].shape)
