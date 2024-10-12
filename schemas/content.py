from pydantic import BaseModel
from datetime import datetime



class ContentCreate(BaseModel):
    title: str
    description: str
    created_by: int  

class ContentUpdate(BaseModel):
    title: str
    description: str

class ContentResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True