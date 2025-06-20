from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_input: str

class QueryResponse(BaseModel):
    result: str
