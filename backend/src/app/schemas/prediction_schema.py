from pydantic import BaseModel

class PredictionRequest(BaseModel):
    income: float
    age: int
    dependents: int
    occupation: int
    city_tier: int
    rent: float
    loan_repayment: float
    insurance: float
    groceries: float
    transport: float
    eating_out: float
    entertainment: float
    utilities: float
    healthcare: float
    education: float
    miscellaneous: float