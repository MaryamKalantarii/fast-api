from fastapi import Depends,APIRouter,status,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from schemas import users as schemas
from models import users as models
from dependencies import get_db
import bcrypt
from accounts.auth import auth_handler

router = APIRouter()



@router.post("/register/",response_model=schemas.ResponseUserRegistrationSchema,
            status_code=status.HTTP_201_CREATED,
)
def account_register(
    request: schemas.UserRegistrationSchema, db: Session = Depends(get_db)):
    if request.password != request.password1:
        raise HTTPException(status_code=400, detail="passwords doest match")

    # جستجوی کاربر با ایمیل خاص در پایگاه داده
    user_obj = (
        db.query(models.UserModel)
        .filter(models.UserModel.email == request.email.lower())
        .first()
    )
    # بررسی وجود کاربر و ایجاد خطا در صورت تکراری بودن ایمیل
    if user_obj:
        raise HTTPException(
            status_code=409,
            detail="user already exists you cannot create another with the same email",
        )

    # رمزنگاری (Encode) کردن رمز عبور
    encoded_password = request.password.encode("utf-8")
    # هش کردن رمز عبور
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    # ایجاد شیء کاربر جدید با رمز عبور هش شده
    user_obj = models.UserModel(
        email=request.email, password=hashed_password.decode("utf-8")
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return JSONResponse(
        {
            "detail": "user has been registered successfully, please go ahead on login"
        },
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login/",
    response_model=schemas.ResponseUserLoginSchema,
    status_code=status.HTTP_200_OK,
)
def account_login(
    request: schemas.UserLoginSchema, db: Session = Depends(get_db)
):
    user_obj = (
        db.query(models.UserModel)
        .filter(models.UserModel.email == request.email)
        .first()
    )

    if not user_obj:
        raise HTTPException(status_code=401, detail="Authentication failed")

    encoded_password = request.password.encode("utf-8")
    if not bcrypt.checkpw(encoded_password, user_obj.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Authentication failed")

    access_token = auth_handler.encode_access_jwt(user_obj.id)
    refresh_token = auth_handler.encode_refresh_jwt(user_obj.id)
    return JSONResponse(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_obj.id,
            "email": request.email,
        },
        status_code=status.HTTP_200_OK,
    )









