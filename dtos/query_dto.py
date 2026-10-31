from pydantic import BaseModel

class QueryItemDTO(BaseModel):
    role: str
    content: str