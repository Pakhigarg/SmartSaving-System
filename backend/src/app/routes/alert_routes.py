from fastapi import APIRouter
from src.app.models.alert_model import create_alert, get_all_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
def read_alerts():
    return get_all_alerts()