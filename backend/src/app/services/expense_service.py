from bson import ObjectId

def create_expense(expense):
    try:
        # user_id fix
        expense["user_id"] = ObjectId(expense["user_id"])

        # 🔥 DATE FIX
        expense["expense_date"] = str(expense["expense_date"])

        result = db.expenses.insert_one(expense)

        return {"message": "Expense added successfully"}

    except Exception as e:
        return {"error": str(e)}