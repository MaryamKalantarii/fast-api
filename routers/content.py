from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from schemas.content import *
from models.content import *

router = APIRouter()

@router.post("/categories/", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # بررسی یکتا بودن نام دسته‌بندی
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    # ایجاد دسته‌بندی جدید
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/categories/{category_id}", response_model=CategoryUpdate)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    # پیدا کردن دسته‌بندی مورد نظر بر اساس ID
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # بررسی یکتا بودن نام جدید (در صورتی که با نام فعلی دسته‌بندی متفاوت باشد)
    if category.name and category.name != db_category.name:
        existing_category = db.query(Category).filter(Category.name == category.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")

    # به‌روزرسانی نام دسته‌بندی
    if category.name:
        db_category.name = category.name

    db.commit()
    db.refresh(db_category)
    return db_category









