from pymongo import MongoClient
from config.config import settings  # assuming settings has Mongo URI
from bson import json_util
client = MongoClient(settings.mongo_db)
db = client[settings.mongo_db]

def execute_query(collection_name: str, query: dict, limit: int = 20):
    collection = db[collection_name]
    results = collection.find(query).limit(limit)
    return [json_util.loads(json_util.dumps(doc)) for doc in results]
