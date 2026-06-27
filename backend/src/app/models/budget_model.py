from bson import ObjectId
from src.database import budgets_collection


def create_budget(budget_data: dict):
    try:
        # user_id convert
        budget_data["user_id"] = ObjectId(budget_data["user_id"])

        result = budgets_collection.insert_one(budget_data)

        return {
            "message": "Budget added successfully",
            "budget_id": str(result.inserted_id)
        }

    except Exception as e:
        return {"error": str(e)}


def get_all_budgets():
    budgets = []
    for budget in budgets_collection.find():
        budget["_id"] = str(budget["_id"])
        budget["user_id"] = str(budget["user_id"])
        budgets.append(budget)
    return budgets