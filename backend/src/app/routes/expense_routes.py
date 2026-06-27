from fastapi import APIRouter

from src.app.schemas.expense_schema import ExpenseSchema

from src.app.models.expense_model import (
    create_expense,
    get_all_expenses,
    delete_expense
)



router = APIRouter(

    prefix="/expenses",

    tags=["Expenses"]

)





# GET EXPENSES

@router.get("/")
def read_expenses():

    return get_all_expenses()





# ADD EXPENSE

@router.post("/")
def add_expense(
    expense: ExpenseSchema
):

    return create_expense(
        expense.dict()
    )





# DELETE EXPENSE

@router.delete("/{id}")
def remove_expense(id:str):

    return delete_expense(id)