import pandas as pd
import numpy as np

from src.app.ml.model_loader import model, label_encoder


def get_recommendation(data):

    # Calculate Total Expense
    total_expense = (
        data.rent
        + data.loan_repayment
        + data.insurance
        + data.groceries
        + data.transport
        + data.eating_out
        + data.entertainment
        + data.utilities
        + data.healthcare
        + data.education
        + data.miscellaneous
    )

    # Create DataFrame in SAME ORDER as model training
    X = pd.DataFrame([[
        data.income,
        data.age,
        data.dependents,
        data.occupation,
        data.city_tier,
        data.rent,
        data.loan_repayment,
        data.insurance,
        data.groceries,
        data.transport,
        data.eating_out,
        data.entertainment,
        data.utilities,
        data.healthcare,
        data.education,
        data.miscellaneous,
        total_expense
    ]], columns=[
        "Income",
        "Age",
        "Dependents",
        "Occupation",
        "City_Tier",
        "Rent",
        "Loan_Repayment",
        "Insurance",
        "Groceries",
        "Transport",
        "Eating_Out",
        "Entertainment",
        "Utilities",
        "Healthcare",
        "Education",
        "Miscellaneous",
        "Total_Expense"
    ])

    # Prediction
    prediction = model.predict(X)

    # Convert numeric prediction to label
    if isinstance(prediction[0], (np.integer, int)):
        category = label_encoder.inverse_transform(prediction)[0]
    else:
        category = str(prediction[0])

    # Recommendation
    if category == "Low":
        recommendation = (
            "Your savings are low. Try reducing eating-out and entertainment expenses."
        )

    elif category == "Medium":
        recommendation = (
            "Your savings are average. Consider creating a monthly budget and increasing savings."
        )

    elif category == "High":
        recommendation = (
            "Excellent! You have strong saving habits. Consider investing your surplus savings."
        )

    else:
        recommendation = "No recommendation available."

    return {
        "predicted_category": category,
        "recommendation": recommendation
    }