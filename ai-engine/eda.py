"""
eda.py — Exploratory Data Analysis for Budget Buddy
Run this FIRST to understand the dataset before any modelling.

What it does:
  1. Prints shape, dtypes, basic stats
  2. Plots distribution of expense amounts
  3. Shows spend by category (bar chart)
  4. Income vs Savings scatter plot
  5. Monthly spending trend
  6. Payment method breakdown (pie chart)
  7. Correlation heatmap
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe for servers)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os, sys

# allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATASET_PATH, PLOTS_DIR, TOP_CATEGORIES, FIGSIZE_STANDARD, FIGSIZE_WIDE


# ─── Utility: save figure ─────────────────────────────────────────────────────
def _save(fig, name: str):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"  [✓] Saved → {path}")


# ─── 1. Load & basic info ─────────────────────────────────────────────────────
def load_and_summarise(path: str = DATASET_PATH) -> pd.DataFrame:
    """Load CSV and print a quick summary to the console."""
    df = pd.read_csv(path, parse_dates=["date"])
    print("=" * 60)
    print("BUDGET BUDDY — Dataset Summary")
    print("=" * 60)
    print(f"  Rows       : {df.shape[0]:,}")
    print(f"  Columns    : {df.shape[1]}")
    print(f"  Date range : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"  Nulls      : {df.isnull().sum().sum()}")
    print()
    print(df.describe(include="all").T.to_string())
    print()
    return df


# ─── 2. Expense-amount distribution ──────────────────────────────────────────
def plot_amount_distribution(df: pd.DataFrame):
    """Histogram of transaction amounts (log-scaled x-axis for clarity)."""
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

    # raw distribution
    axes[0].hist(df["amount"], bins=60, color="#4C72B0", edgecolor="white")
    axes[0].set_title("Expense Amount Distribution")
    axes[0].set_xlabel("Amount (₹)")
    axes[0].set_ylabel("Frequency")

    # log-scale (reveals shape better when range is wide)
    axes[1].hist(df["amount"], bins=60, color="#DD8452", edgecolor="white", log=True)
    axes[1].set_title("Expense Amount (log scale)")
    axes[1].set_xlabel("Amount (₹)")
    axes[1].set_ylabel("Frequency (log)")

    fig.suptitle("Expense Amount Distributions", fontsize=14, fontweight="bold")
    _save(fig, "01_amount_distribution.png")


# ─── 3. Spend by category ─────────────────────────────────────────────────────
def plot_category_spend(df: pd.DataFrame):
    """Horizontal bar chart — total spend per expense category."""
    top = (df.groupby("category")["amount"]
             .sum()
             .sort_values(ascending=False)
             .head(TOP_CATEGORIES))

    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)
    bars = ax.barh(top.index[::-1], top.values[::-1], color="#55A868")
    ax.bar_label(bars, fmt="₹{:,.0f}", padding=4, fontsize=8)
    ax.set_title("Total Spend by Category (Top 10)", fontweight="bold")
    ax.set_xlabel("Total Amount (₹)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    _save(fig, "02_spend_by_category.png")


# ─── 4. Income vs Savings scatter ─────────────────────────────────────────────
def plot_income_vs_savings(df: pd.DataFrame):
    """Scatter plot to see if higher income leads to more savings."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)
    ax.scatter(df["income"], df["savings"], alpha=0.3, s=10, color="#C44E52")
    ax.set_title("Income vs Savings", fontweight="bold")
    ax.set_xlabel("Income (₹)")
    ax.set_ylabel("Savings (₹)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    _save(fig, "03_income_vs_savings.png")


# ─── 5. Monthly spending trend ────────────────────────────────────────────────
def plot_monthly_trend(df: pd.DataFrame):
    """Line chart — average monthly spend over time."""
    monthly = (df.set_index("date")["amount"]
                 .resample("ME")        # Month-End frequency
                 .mean()
                 .reset_index())

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.plot(monthly["date"], monthly["amount"], linewidth=1.5, color="#8172B2")
    ax.fill_between(monthly["date"], monthly["amount"], alpha=0.15, color="#8172B2")
    ax.set_title("Average Monthly Expense Trend", fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    fig.autofmt_xdate()
    _save(fig, "04_monthly_trend.png")


# ─── 6. Payment method pie chart ─────────────────────────────────────────────
def plot_payment_methods(df: pd.DataFrame):
    """Pie chart showing how people pay."""
    counts = df["payment_method"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        startangle=140, pctdistance=0.82
    )
    for t in autotexts:
        t.set_fontsize(8)
    ax.set_title("Payment Method Breakdown", fontweight="bold", fontsize=13)
    _save(fig, "05_payment_methods.png")


# ─── 7. Correlation heatmap ───────────────────────────────────────────────────
def plot_correlation_heatmap(df: pd.DataFrame):
    """Heatmap of numeric column correlations — reveals multicollinearity."""
    import numpy as np
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(numeric_cols, fontsize=8)

    # annotate each cell
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center", fontsize=7,
                    color="white" if abs(corr.iloc[i, j]) > 0.6 else "black")

    ax.set_title("Correlation Heatmap (Numeric Features)", fontweight="bold")
    _save(fig, "06_correlation_heatmap.png")


# ─── Weekday vs Weekend spend ─────────────────────────────────────────────────
def plot_day_type_spend(df: pd.DataFrame):
    """Box plot comparing weekend vs weekday transaction amounts."""
    fig, ax = plt.subplots(figsize=(7, 5))
    groups = [df[df["day_type"] == g]["amount"].values for g in ["Weekday", "Weekend"]]
    ax.boxplot(groups, labels=["Weekday", "Weekend"], patch_artist=True,
               boxprops=dict(facecolor="#4C72B0", alpha=0.6))
    ax.set_title("Weekday vs Weekend Spend", fontweight="bold")
    ax.set_ylabel("Amount (₹)")
    ax.set_yscale("log")
    _save(fig, "07_daytype_spend.png")


# ─── Entry point ──────────────────────────────────────────────────────────────
def run_eda(path: str = DATASET_PATH) -> pd.DataFrame:
    """Run all EDA steps and return the loaded DataFrame."""
    print("\n🔍  Running EDA …")
    df = load_and_summarise(path)
    plot_amount_distribution(df)
    plot_category_spend(df)
    plot_income_vs_savings(df)
    plot_monthly_trend(df)
    plot_payment_methods(df)
    plot_correlation_heatmap(df)
    plot_day_type_spend(df)
    print("\n✅  EDA complete — all plots saved to /plots/\n")
    return df


if __name__ == "__main__":
    run_eda()

