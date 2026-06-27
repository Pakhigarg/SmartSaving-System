from pydantic import BaseModel

class BudgetSchema(BaseModel):
    user_id: str
    category: str
    month: int
    year: int
    budget_amount: float