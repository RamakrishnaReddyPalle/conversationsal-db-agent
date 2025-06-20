from src.agent.schema_explorer import get_collections, get_schema

def cache_metadata():
    meta = {}
    for coll in get_collections():
        meta[coll] = get_schema(coll)
    return meta
