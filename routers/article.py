from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
from schemas import article as schemas
from models import article as models
from dependencies import get_db
import os


router = APIRouter()



router = APIRouter()

@router.post("/article/", response_model=schemas.Article)
async def create_article(
    title: str = Form(..., min_length=3, max_length=20),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # تعریف مسیر ذخیره‌سازی فایل تصویر
    images_directory = "images"
    
    # چک کردن وجود دایرکتوری و ایجاد آن در صورت عدم وجود
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

    # بررسی پسوند فایل تصویر
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="فقط فرمت‌های png و jpeg مجاز هستند")
        
        file_location = f"{images_directory}/{image.filename}"
        
        # ذخیره فایل تصویر
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_filename = image.filename
    else:
        image_filename = None

    # ایجاد شی دیتابیس
    new_article = models.Article(
        title=title,
        description=description,
        image=image_filename
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

