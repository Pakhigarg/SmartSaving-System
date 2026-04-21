
# ============================================================
#   BUDGET BUDDY — Data Preparation Pipeline
#   Author  : [Your Name]
#   Course  : [Your Course Name]
#   Date    : April 2026
#   Purpose : Merge, clean & export master training dataset
#             from 4 raw financial data sources
# ============================================================

# ── 0. Install / import libraries ───────────────────────────────────────────
# (Uncomment the line below if running in Google Colab for the first time)
# !pip install pandas numpy --quiet

import pandas as pd
import numpy as np
import random
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")
random.seed(42)
np.random.seed(42)

print("=" * 60)
print("   BUDGET BUDDY — Data Preparation Pipeline")
print("=" * 60)


# ── 1. Load raw datasets ─────────────────────────────────────────────────────
# If running in Google Colab, upload the 4 CSV files using:
#   from google.colab import files
#   files.upload()
# Then update the file paths below accordingly.

print("\n[STEP 1] Loading raw datasets...")

personal_finance = pd.read_csv("personal_finance_tracker_dataset.csv")
indian_finance   = pd.read_csv("Indian_Personal_Finance_Behavior_Dataset_2026.csv")
student_spending = pd.read_csv("student_spending (1).csv")
cards_data       = pd.read_csv("cards_data.csv")

print(f"  ✔  Personal Finance Tracker : {personal_finance.shape[0]:>5} rows, {personal_finance.shape[1]} columns")
print(f"  ✔  Indian Personal Finance  : {indian_finance.shape[0]:>5} rows, {indian_finance.shape[1]} columns")
print(f"  ✔  Student Spending         : {student_spending.shape[0]:>5} rows, {student_spending.shape[1]} columns")
print(f"  ✔  Cards Data               : {cards_data.shape[0]:>5} rows, {cards_data.shape[1]} columns")


# ── 2. Define helper utilities ───────────────────────────────────────────────

def generate_random_dates(n, start="2020-01-01", end="2025-12-31"):
    """Generate n random date strings between start and end."""
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    delta    = (datetime.strptime(end, "%Y-%m-%d") - start_dt).days
    return [(start_dt + timedelta(days=int(d))).strftime("%Y-%m-%d")
            for d in np.random.randint(0, delta, n)]

def get_day_type(date_series):
    """Return 'Weekend' or 'Weekday' for each date in a Series."""
    return pd.to_datetime(date_series).dt.dayofweek.map(
        lambda x: "Weekend" if x >= 5 else "Weekday"
    )

# Unified payment method labels across all sources
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'UPI', 'Cash', 'Net Banking']

# Final schema — 11 features
FINAL_COLUMNS = [
    'date', 'amount', 'category', 'payment_method',
    'income', 'food', 'transport', 'shopping',
    'savings', 'budget', 'day_type'
]


# ── 3. Transform each dataset into the unified schema ────────────────────────
print("\n[STEP 2] Transforming datasets into unified schema...")

# ── 3a. Personal Finance Tracker ─────────────────────────────────────────────
# Columns used: date, monthly_income, budget_goal, essential_spending,
#               discretionary_spending, actual_savings, category

df_pf = pd.DataFrame()
df_pf['date']           = personal_finance['date']
df_pf['amount']         = (personal_finance['essential_spending'] +
                            personal_finance['discretionary_spending']).round(2)
df_pf['category']       = personal_finance['category']
df_pf['payment_method'] = np.random.choice(
                            PAYMENT_METHODS, len(personal_finance),
                            p=[0.25, 0.25, 0.25, 0.15, 0.10])
df_pf['income']         = personal_finance['monthly_income'].round(2)
df_pf['food']           = (personal_finance['essential_spending'] * 0.35).round(2)
df_pf['transport']      = (personal_finance['essential_spending'] * 0.15).round(2)
df_pf['shopping']       = (personal_finance['discretionary_spending'] * 0.40).round(2)
df_pf['savings']        = personal_finance['actual_savings'].round(2)
df_pf['budget']         = personal_finance['budget_goal'].round(2)
df_pf['day_type']       = get_day_type(df_pf['date'])

print(f"  ✔  Personal Finance Tracker transformed : {len(df_pf)} rows")

# ── 3b. Indian Personal Finance ───────────────────────────────────────────────
# Columns used: Monthly_Income_INR, Monthly_Expenses_INR,
#               Savings_Percentage, Primary_Financial_Goal, Savings_Channel

goal_to_category = {
    'Home Purchase':      'Bills & Utilities',
    'Wealth Accumulation':'Investments',
    'Retirement':         'Investments',
    'Education':          'Education',
    'Emergency Fund':     'Healthcare',
    'Travel':             'Travel',
    'Debt Repayment':     'Bills & Utilities',
    'Marriage':           'Shopping',
}

channel_to_payment = {
    'Digital Wallet': 'Mobile Wallet',
    'Bank Account':   'Net Banking',
    'Fixed Deposit':  'Net Banking',
    'Mutual Funds':   'Net Banking',
    'Cash':           'Cash',
    'Stock Market':   'Net Banking',
    'PPF':            'Net Banking',
}

df_ind = pd.DataFrame()
df_ind['date']           = generate_random_dates(len(indian_finance), "2023-01-01", "2026-03-31")
df_ind['amount']         = indian_finance['Monthly_Expenses_INR'].round(2)
df_ind['category']       = indian_finance['Primary_Financial_Goal'].map(goal_to_category).fillna('Investments')
df_ind['payment_method'] = indian_finance['Savings_Channel'].map(channel_to_payment).fillna('UPI')
df_ind['income']         = indian_finance['Monthly_Income_INR'].round(2)
df_ind['food']           = (indian_finance['Monthly_Expenses_INR'] * 0.28).round(2)
df_ind['transport']      = (indian_finance['Monthly_Expenses_INR'] * 0.12).round(2)
df_ind['shopping']       = (indian_finance['Monthly_Expenses_INR'] * 0.18).round(2)
df_ind['savings']        = (indian_finance['Monthly_Income_INR'] *
                             indian_finance['Savings_Percentage'] / 100).round(2)
df_ind['budget']         = (indian_finance['Monthly_Income_INR'] * 0.80).round(2)
df_ind['day_type']       = get_day_type(df_ind['date'])

print(f"  ✔  Indian Personal Finance transformed  : {len(df_ind)} rows")

# ── 3c. Student Spending ──────────────────────────────────────────────────────
# Columns used: monthly_income, financial_aid, food, transportation,
#               entertainment, housing, tuition, books_supplies,
#               personal_care, technology, health_wellness,
#               miscellaneous, preferred_payment_method

expense_cols   = ['food', 'transportation', 'entertainment', 'housing',
                  'tuition', 'books_supplies', 'personal_care',
                  'technology', 'health_wellness', 'miscellaneous']
total_expense  = student_spending[expense_cols].sum(axis=1)
total_income   = student_spending['monthly_income'] + student_spending['financial_aid']
student_saving = (total_income - total_expense).clip(lower=0)

student_pm_map = {
    'Credit/Debit Card': 'Debit Card',
    'Cash':              'Cash',
    'Mobile Payment':    'Mobile Wallet',
    'Bank Transfer':     'Net Banking',
}

df_st = pd.DataFrame()
df_st['date']           = generate_random_dates(len(student_spending), "2021-01-01", "2025-12-31")
df_st['amount']         = total_expense.round(2)
df_st['category']       = np.random.choice(
                            ['Education', 'Food & Dining', 'Entertainment',
                             'Shopping', 'Transport', 'Groceries'],
                            len(student_spending),
                            p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10])
df_st['payment_method'] = student_spending['preferred_payment_method'].map(student_pm_map).fillna('Debit Card')
df_st['income']         = total_income.round(2)
df_st['food']           = student_spending['food'].round(2)
df_st['transport']      = student_spending['transportation'].round(2)
df_st['shopping']       = (student_spending['entertainment'] +
                            student_spending['personal_care']).round(2)
df_st['savings']        = student_saving.round(2)
df_st['budget']         = (total_income * 0.85).round(2)
df_st['day_type']       = get_day_type(df_st['date'])

print(f"  ✔  Student Spending transformed         : {len(df_st)} rows")

# ── 3d. Cards Data ────────────────────────────────────────────────────────────
# Columns used: card_type, card_brand, credit_limit, acct_open_date
# Strategy: credit_limit × 0.40 = estimated monthly income (bank rule-of-thumb)

cards_data['credit_limit_clean'] = (
    cards_data['credit_limit']
    .astype(str)
    .str.replace(r'[\$,]', '', regex=True)
    .str.strip()
)
cards_data['credit_limit_clean'] = pd.to_numeric(cards_data['credit_limit_clean'], errors='coerce')

cards_data['date_parsed'] = pd.to_datetime(
    cards_data['acct_open_date'], format='%m/%Y', errors='coerce'
).dt.strftime('%Y-%m-%d')

income_cards  = (cards_data['credit_limit_clean'] * 0.40).round(2)
txn_rate      = np.random.uniform(0.04, 0.14, len(cards_data))
amount_cards  = (income_cards * txn_rate).round(2)
card_pm_label = (cards_data['card_type'].str.strip() +
                 ' (' + cards_data['card_brand'].str.strip() + ')')

# Fill any missing dates with random generated dates
fallback_dates = pd.Series(generate_random_dates(len(cards_data), "2019-01-01", "2024-12-31"))
date_cards     = cards_data['date_parsed'].fillna(fallback_dates)

df_cd = pd.DataFrame()
df_cd['date']           = date_cards
df_cd['amount']         = amount_cards
df_cd['category']       = np.random.choice(
                            ['Shopping', 'Travel', 'Food & Dining', 'Bills & Utilities',
                             'Entertainment', 'Healthcare', 'Groceries'],
                            len(cards_data),
                            p=[0.20, 0.10, 0.20, 0.20, 0.10, 0.10, 0.10])
df_cd['payment_method'] = card_pm_label
df_cd['income']         = income_cards
df_cd['food']           = (amount_cards * 0.25).round(2)
df_cd['transport']      = (amount_cards * 0.10).round(2)
df_cd['shopping']       = (amount_cards * 0.30).round(2)
df_cd['savings']        = (income_cards * np.random.uniform(0.05, 0.22, len(cards_data))).round(2)
df_cd['budget']         = (income_cards * 0.75).round(2)
df_cd['day_type']       = get_day_type(df_cd['date'])

print(f"  ✔  Cards Data transformed               : {len(df_cd)} rows")


# ── 4. Merge all four datasets ───────────────────────────────────────────────
print("\n[STEP 3] Merging all datasets...")

master = pd.concat(
    [df_pf[FINAL_COLUMNS],
     df_ind[FINAL_COLUMNS],
     df_st[FINAL_COLUMNS],
     df_cd[FINAL_COLUMNS]],
    ignore_index=True
)

print(f"  ✔  Total rows after merge : {len(master):,}")


# ── 5. Data Cleaning ─────────────────────────────────────────────────────────
print("\n[STEP 4] Cleaning data...")

# 5a. Coerce numeric columns
numeric_cols = ['amount', 'income', 'food', 'transport', 'shopping', 'savings', 'budget']
for col in numeric_cols:
    master[col] = pd.to_numeric(master[col], errors='coerce').round(2)

rows_before = len(master)

# 5b. Drop rows with any missing values
master.dropna(inplace=True)
print(f"  ✔  Rows dropped (missing values)  : {rows_before - len(master)}")

# 5c. Remove rows where core financial values are zero or negative
rows_after_na = len(master)
master = master[(master['amount'] > 0) & (master['income'] > 0)]
print(f"  ✔  Rows dropped (invalid amounts) : {rows_after_na - len(master)}")

# 5d. Remove exact duplicate rows
rows_after_invalid = len(master)
master.drop_duplicates(inplace=True)
print(f"  ✔  Rows dropped (duplicates)      : {rows_after_invalid - len(master)}")

# 5e. Sort by date (ascending) and reset index
master['date'] = pd.to_datetime(master['date'])
master.sort_values('date', inplace=True)
master['date'] = master['date'].dt.strftime('%Y-%m-%d')
master.reset_index(drop=True, inplace=True)

print(f"\n  ✔  Final clean dataset shape : {master.shape}")


# ── 6. Exploratory summary ───────────────────────────────────────────────────
print("\n[STEP 5] Dataset summary...")

print(f"\n  Shape              : {master.shape[0]:,} rows × {master.shape[1]} columns")
print(f"\n  Missing values     :\n{master.isnull().sum().to_string()}")

print(f"\n  Category distribution :")
print(master['category'].value_counts().to_string())

print(f"\n  Payment method distribution :")
print(master['payment_method'].value_counts().head(10).to_string())

print(f"\n  Day type distribution :")
print(master['day_type'].value_counts().to_string())

print(f"\n  Numeric feature statistics :")
print(master[numeric_cols].describe().round(2).to_string())

print(f"\n  Date range : {master['date'].min()}  →  {master['date'].max()}")


# ── 7. Export ────────────────────────────────────────────────────────────────
print("\n[STEP 6] Saving dataset...")

output_path = "budget_buddy_master_dataset.csv"
master.to_csv(output_path, index=False)

print(f"  ✔  Saved as  : {output_path}")
print(f"  ✔  Rows      : {len(master):,}")
print(f"  ✔  Columns   : {list(master.columns)}")

print("\n" + "=" * 60)
print("   Dataset preparation complete! Ready for model training.")
print("=" * 60)
