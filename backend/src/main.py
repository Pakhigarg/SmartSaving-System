from fastapi import FastAPI
from src.routes import auth
from src.routes import expense

app = FastAPI(
    title="Budget Buddy Backend"
)


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(
    expense.router,
    prefix="/expense",
    tags=["Expense"]
)


@app.get("/")
def home():
    return {
        "message": "Budget Buddy API Running"
    }