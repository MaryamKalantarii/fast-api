from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import List
from schemas import content as schemas
from models import content as models
from models.users import UserModel 

from dependencies import get_db


router = APIRouter()

@router.post("/contents/", response_model=schemas.ContentResponse)
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db)):
    # استفاده از User که از accounts.models.users ایمپورت شده است
    user = db.query(UserModel).filter(UserModel.id == content.created_by).first()  
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_content = models.Content(title=content.title, description=content.description, created_by=content.created_by)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@router.get("/contents/", response_model=List[schemas.ContentResponse])
def get_contents(db: Session = Depends(get_db)):
    return db.query(models.Content).all()

@router.get("/contents/{content_id}", response_model=schemas.ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/contents/{content_id}", response_model=schemas.ContentResponse)
def update_content(content_id: int, content_data: schemas.ContentUpdate, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.title = content_data.title
    content.description = content_data.description
    db.commit()
    db.refresh(content)
    return content

@router.delete("/contents/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return {"detail": "Content deleted successfully"}












