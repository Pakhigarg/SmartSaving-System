"""
config.py — Central configuration for Budget Buddy AI Engine
All paths, model parameters, and feature lists live here.
Change once → takes effect everywhere.
"""

import os

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
MODEL_DIR   = os.path.join(BASE_DIR, "models")
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR   = os.path.join(BASE_DIR, "plots")

DATASET_PATH          = os.path.join(DATA_DIR, "budget_buddy_master_dataset.csv")

# ── Original models ───────────────────────────────────────────────────────────
REGRESSION_MODEL_PATH = os.path.join(MODEL_DIR, "regression_model.joblib")
CLUSTER_MODEL_PATH    = os.path.join(MODEL_DIR, "cluster_model.joblib")
SCALER_PATH           = os.path.join(MODEL_DIR, "scaler.joblib")
CLUSTER_SCALER_PATH   = os.path.join(MODEL_DIR, "cluster_scaler.joblib")

# ── New model paths (v2) ──────────────────────────────────────────────────────
BUDGET_MODEL_PATH     = os.path.join(MODEL_DIR, "budget_classifier.joblib")
BUDGET_SCALER_PATH    = os.path.join(MODEL_DIR, "budget_scaler.joblib")
CATEGORY_MODEL_PATH   = os.path.join(MODEL_DIR, "category_classifier.joblib")
CATEGORY_SCALER_PATH  = os.path.join(MODEL_DIR, "category_scaler.joblib")
FORECAST_MODEL_PATH   = os.path.join(MODEL_DIR, "forecast_model.joblib")

# ─── Feature lists ────────────────────────────────────────────────────────────
# Features used to predict expense amount (regression target = 'amount')
REGRESSION_FEATURES = [
    "income", "food", "transport", "shopping", "savings", "budget",
    "is_weekend", "expense_ratio", "savings_rate", "food_ratio",
    "transport_ratio", "shopping_ratio", "budget_utilization",
    "month", "quarter",
    "category_encoded", "payment_encoded"
]

# Features used for clustering (user behaviour segments)
CLUSTER_FEATURES = [
    "income", "savings", "budget",
    "expense_ratio", "savings_rate", "food_ratio",
    "transport_ratio", "shopping_ratio", "budget_utilization",
    "avg_transaction"
]

# Features for budget exceeded classifier (Model 2)
# We use financial ratios only — these are known BEFORE the transaction
BUDGET_FEATURES = [
    "income", "savings", "budget",
    "expense_ratio", "savings_rate", "budget_utilization",
    "food_ratio", "transport_ratio", "shopping_ratio",
    "month", "quarter", "is_weekend"
]

# Features for category predictor (Model 3)
# Given amount + payment + time, predict which category
CATEGORY_FEATURES = [
    "amount", "income", "food", "transport", "shopping",
    "savings", "budget", "is_weekend", "month", "quarter",
    "payment_encoded", "expense_ratio", "budget_utilization"
]

# ─── Model hyper-parameters ───────────────────────────────────────────────────
REGRESSION_PARAMS = {
    "n_estimators": 200,
    "max_depth": 10,
    "min_samples_split": 5,
    "random_state": 42,
    "n_jobs": -1
}

CLUSTER_PARAMS = {
    "n_clusters": 4,
    "random_state": 42,
    "n_init": 10,
    "max_iter": 300
}

BUDGET_CLASSIFIER_PARAMS = {
    "C": 1.0,
    "max_iter": 1000,
    "random_state": 42
}

CATEGORY_CLASSIFIER_PARAMS = {
    "n_estimators": 150,
    "max_depth": 8,
    "random_state": 42,
    "n_jobs": -1
}

# Cluster human-readable labels
CLUSTER_LABELS = {
    0: "Frugal Saver",
    1: "Balanced Spender",
    2: "High Earner",
    3: "Impulse Buyer"
}

# ─── EDA settings ─────────────────────────────────────────────────────────────
TOP_CATEGORIES   = 10
FIGSIZE_STANDARD = (10, 6)
FIGSIZE_WIDE     = (14, 6)
RANDOM_STATE     = 42

