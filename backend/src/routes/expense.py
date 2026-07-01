from fastapi import APIRouter, Depends

from src.database.mongodb import expenses_collection
from src.schemas.expense_schema import ExpenseCreate
from src.utils.auth_dependency import get_current_user


router = APIRouter()


@router.post("/add")
def add_expense(
    expense: ExpenseCreate,
    user = Depends(get_current_user)
):

    new_expense = {

        "user_email": user["email"],
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date
    }


    expenses_collection.insert_one(new_expense)


    return {
        "message": "Expense Added Successfully"
    }



@router.get("/")
def get_expenses(
    user = Depends(get_current_user)
):

    expenses = list(
        expenses_collection.find(
            {
                "user_email": user["email"]
            },
            {
                "_id":0
            }
        )
    )


    return expenses