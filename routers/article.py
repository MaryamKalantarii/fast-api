# from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import shutil
# from schemas import article as schemas
# from models import article as models
# from dependencies import get_db
# import os
# import shutil

# router = APIRouter()

# @router.post("/article/", response_model=schemas.Article)
# async def create_article(
#     article_data: schemas.ArticleBase,
#     image: Optional[UploadFile] = File(None),
#     db: Session = Depends(get_db)
# ):
#     # تعریف مسیر ذخیره‌سازی فایل تصویر
#     images_directory = "images"
    
#     # چک کردن وجود دایرکتوری و ایجاد آن در صورت عدم وجود
#     if not os.path.exists(images_directory):
#         os.makedirs(images_directory)

#     image_filename = None
#     if image:
#         # اعتبارسنجی تصویر با استفاده از schema
#         image_data = schemas.ImageUpload(
#             filename=image.filename,
#             content_type=image.content_type
#         )

#         file_location = f"{images_directory}/{image_data.filename}"
        
#         # ذخیره فایل تصویر
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
#         image_filename = image_data.filename

#     # ایجاد شی دیتابیس
#     new_article = models.Article(
#         title=article_data.title,
#         description=article_data.description,
#         image=image_filename
#     )
#     db.add(new_article)
#     db.commit()
#     db.refresh(new_article)

#     return new_article

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil

from schemas import article as schemas
from models import article as models
from dependencies import get_db

router = APIRouter()
BASE_URL = "http://127.0.0.1:8000/image/"

@router.post("/article/", response_model=schemas.Article)
async def create_article(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # تعریف مسیر ذخیره‌سازی فایل تصویر
    images_directory = "image/"
    
    # چک کردن وجود دایرکتوری و ایجاد آن در صورت عدم وجود
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

     # مدیریت فایل تصویر
    image_filename = None
    if image:
        # اعتبارسنجی تصویر با استفاده از schema
        try:
            image_data = schemas.ImageUpload(
                filename=image.filename,
                content_type=image.content_type
            )
        except ValueError:
            # اگر فرمت تصویر نامعتبر باشد، یک خطای HTTP برمی‌گردانیم
            raise HTTPException(status_code=400, detail="فقط فرمت‌های png و jpeg مجاز هستند")

        file_location = f"{images_directory}/{image_data.filename}"
        

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
