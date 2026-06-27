from src.database import alerts_collection


def create_alert(alert_data: dict):
    result = alerts_collection.insert_one(alert_data)
    return {
        "message": "Alert generated",
        "alert_id": str(result.inserted_id)
    }


def get_all_alerts():
    alerts = []
    for alert in alerts_collection.find():
        alert["_id"] = str(alert["_id"])
        alerts.append(alert)
    return alerts