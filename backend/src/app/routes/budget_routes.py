from fastapi import APIRouter
from src.app.schemas.budget_schema import BudgetSchema
from src.app.models.budget_model import create_budget, get_all_budgets

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/")
def add_budget(budget: BudgetSchema):
    return create_budget(budget.model_dump())


@router.get("/")
def read_budgets():
    return get_all_budgets()