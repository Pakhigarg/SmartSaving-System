from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.routes.user_routes import router as user_router
from src.app.routes.expense_routes import router as expense_router
from src.app.routes.budget_routes import router as budget_router
from src.app.routes.alert_routes import router as alert_router
from src.app.routes.recommendation_routes import router as recommendation_router


app = FastAPI(
    title="Budget Buddy API"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



@app.get("/")
def home():

    return {
        "message":
        "Backend running successfully 🚀"
    }



# Routes

app.include_router(user_router)

app.include_router(expense_router)

app.include_router(budget_router)

app.include_router(alert_router)

app.include_router(recommendation_router)