from bson import ObjectId

from src.database import (
    expenses_collection,
    budgets_collection
)

from src.app.models.alert_model import create_alert
from src.app.models.recommendation_model import create_recommendation



# CREATE EXPENSE
def create_expense(expense_data: dict):

    try:

        # convert user id
        if "user_id" in expense_data:
            expense_data["user_id"] = ObjectId(
                expense_data["user_id"]
            )


        # amount convert
        expense_data["amount"] = float(
            expense_data["amount"]
        )


        # date handle
        if "date" in expense_data:
            expense_data["expense_date"] = expense_data.pop("date")


        # insert expense
        result = expenses_collection.insert_one(
            expense_data
        )


        user_id = expense_data["user_id"]
        category = expense_data["category"]



        # calculate category spending

        expenses = expenses_collection.find({
            "user_id": user_id,
            "category": category
        })


        total = 0

        for exp in expenses:
            total += exp["amount"]



        # check budget

        budget = budgets_collection.find_one({
            "user_id": user_id,
            "category": category
        })


        if budget:

            if total > budget["budget_amount"]:


                alert_data = {

                    "user_id": str(user_id),

                    "message":
                    f"Budget exceeded for {category}",

                    "total_spent": total
                }


                create_alert(alert_data)



                recommendation_data = {

                    "user_id":str(user_id),

                    "message":
                    f"You are overspending on {category}"
                }


                create_recommendation(
                    recommendation_data
                )



        return {

            "message":
            "Expense added successfully",

            "expense_id":
            str(result.inserted_id)

        }


    except Exception as e:

        return {

            "error":str(e)

        }





# GET ALL EXPENSES

def get_all_expenses():

    expenses=[]


    for expense in expenses_collection.find():


        expenses.append({

            "id":
            str(expense["_id"]),


            "title":
            expense["title"],


            "amount":
            expense["amount"],


            "category":
            expense["category"],


            "date":
            expense.get(
                "expense_date",
                ""
            )

        })


    return expenses





# DELETE EXPENSE

def delete_expense(id:str):

    try:


        result = expenses_collection.delete_one({

            "_id":
            ObjectId(id)

        })



        if result.deleted_count == 1:


            return {

                "message":
                "Expense deleted successfully"

            }


        else:


            return {

                "message":
                "Expense not found"

            }



    except Exception as e:


        return {

            "error":
            str(e)

        }