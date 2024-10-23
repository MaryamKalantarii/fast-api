from fastapi import Depends, HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from schemas.content import *
from models.content import *
from accounts.auth.auth_bearer import JWTBearer
from dependencies import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas import content as schemas
from models import content as models

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




@router.post("/user/post/")
async def post_create(
    request: schemas.PostSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer()),
):
    # ایجاد پست جدید
    post_obj = models.PostModel(
        title=request.title,
        content=request.content,
        is_published=request.is_published,
        user=user_id,
    )

    # اضافه کردن دسته‌بندی‌ها به پست
    if request.categories:
        # جستجوی دسته‌بندی‌ها در دیتابیس و اضافه کردن آن‌ها به پست
        categories = db.query(models.Category).filter(models.Category.id.in_(request.categories)).all()
        post_obj.categories = categories

    # ذخیره کردن پست در دیتابیس
    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)

    # بازگشت پاسخ به کلاینت
    return JSONResponse(
        jsonable_encoder(schemas.AuthorPostResponse.from_orm(post_obj)),
        status_code=status.HTTP_201_CREATED,
    )



@router.put("/user/post/{id}/")
async def post_update(
    id: int,
    request: schemas.PostUpdateSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer()),
):
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id, models.PostModel.user == user_id
    ).first()
    
    if not post_obj:
        raise HTTPException(status_code=404, detail="post not found")
    
    # به روز رسانی مقادیر دیگر
    if request.title is not None:
        post_obj.title = request.title
    if request.content is not None:
        post_obj.content = request.content
    if request.is_published is not None:
        post_obj.is_published = request.is_published
    
    # به روز رسانی دسته‌بندی‌ها
    if request.categories is not None:
        post_obj.categories.clear()  # پاک کردن دسته‌بندی‌های قبلی
        post_obj.categories.extend(db.query(models.Category).filter(models.Category.id.in_(request.categories)).all())
    
    db.commit()
    
    return JSONResponse(
        content=jsonable_encoder(
            schemas.AuthorPostResponse.from_orm(post_obj)
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )





