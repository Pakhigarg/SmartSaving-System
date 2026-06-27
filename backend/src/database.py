from pymongo import MongoClient
from src.config import MONGO_URL

client = MongoClient(MONGO_URL)

db = client["smart_saving_system"]

users_collection = db["users"]
expenses_collection = db["expenses"]
budgets_collection = db["budgets"]
goals_collection = db["savings_goals"]
alerts_collection = db["alerts"]
recommendations_collection = db["recommendations"]

if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully")
    except Exception as e:
        print("MongoDB connection failed:", e)