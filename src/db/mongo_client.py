from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

uri = f"mongodb+srv://{user}:{password}@sylvr-financial-cluster.jz9cn66.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
DB_NAME = os.getenv("DATABASE_NAME")
db = client[DB_NAME]

def get_collection(collection_name):
    return db[collection_name]
