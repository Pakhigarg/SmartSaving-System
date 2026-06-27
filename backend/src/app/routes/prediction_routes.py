from fastapi import APIRouter

from app.schemas.prediction_schema import PredictionRequest
from app.services.prediction_service import predict_savings

router = APIRouter()


@router.post("/predict")
def predict(data: PredictionRequest):

    prediction = predict_savings(data)

    return {
        "status": "success",
        "prediction": prediction
    }