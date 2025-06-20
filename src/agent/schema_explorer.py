from src.db.mongo_client import get_db

def get_collections():
    db = get_db()
    return db.list_collection_names()

def get_schema(collection_name):
    db = get_db()
    return db[collection_name].find_one()
