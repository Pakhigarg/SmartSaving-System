from app.ml.model_loader import model, label_encoder


def predict_savings(data):

    # Calculate Total Expense
    total_expense = (
        data.rent +
        data.loan_repayment +
        data.insurance +
        data.groceries +
        data.transport +
        data.eating_out +
        data.entertainment +
        data.utilities +
        data.healthcare +
        data.education +
        data.miscellaneous
    )

    # Arrange features in the SAME ORDER as used during training
    features = [[
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
    ]]

    # Predict
    prediction = model.predict(features)

    # Convert numeric prediction back to text
    category = label_encoder.inverse_transform(prediction)

    return category[0]