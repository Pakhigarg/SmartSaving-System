from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExpenseSchema(BaseModel):
    user_id: str
    title: str
    amount: float
    category: str
    expense_date: date
    payment_method: Optional[str] = None
    notes: Optional[str] = None