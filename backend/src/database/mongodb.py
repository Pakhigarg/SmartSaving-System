from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["BudgetBuddy"]

users_collection = db["users"]
expenses_collection = db["expenses"]
budgets_collection = db["budgets"]
goals_collection = db["goals"]

print("MongoDB Connected")