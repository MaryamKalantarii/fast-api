from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


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


