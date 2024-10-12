from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from schemas import users as schemas
from models import users as models
from dependencies import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    db_user =models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()













