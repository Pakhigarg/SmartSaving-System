from fastapi import APIRouter
from src.app.schemas.prediction_schema import PredictionRequest
from src.app.services.recommendation_service import get_recommendation

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

@router.post("/")
def generate_recommendation(data: PredictionRequest):
    return get_recommendation(data)