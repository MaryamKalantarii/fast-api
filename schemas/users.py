from pydantic import BaseModel,EmailStr
from typing import List,Optional

# class UserCreate(BaseModel):
#     username: str
#     email: str

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str

#     class Config:
#         from_attributes = True

class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    password1: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "maryam@gmail.com",
                "password": "yourpassword",
                "password1": "yourpassword",
            }
        }



        
class ResponseUserRegistrationSchema(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {"example": {"detail": "message content"}}




class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "maryam@gmail.com",
                "password": "yourpassword",
            }
        }