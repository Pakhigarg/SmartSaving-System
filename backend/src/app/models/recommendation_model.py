from src.database import recommendations_collection

def create_recommendation(data: dict):
    result = recommendations_collection.insert_one(data)
    return {
        "message": "Recommendation generated",
        "id": str(result.inserted_id)
    }

def get_all_recommendations():
    recs = []
    for r in recommendations_collection.find():
        r["_id"] = str(r["_id"])
        recs.append(r)
    return recs