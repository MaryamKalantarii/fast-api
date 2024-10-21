from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema برای ایجاد پست جدید
class PostSchema(BaseModel):
    title: str
    content: str
    is_published: bool
    categories: Optional[List[int]]  # لیستی از شناسه‌های دسته‌بندی‌ها

# Schema برای به‌روزرسانی پست
class PostUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str] 
    is_published: Optional[bool] 
    categories: Optional[List[int]]   # لیستی از شناسه‌های دسته‌بندی‌ها

# Schema برای بازگرداندن اطلاعات پست
class PostResponse(BaseModel):
    id: Optional[int]
    title: str
    user: int
    content: str
    created_at: Optional[datetime] 
    modified_at: Optional[datetime] 
    categories: Optional[List[int]]  # لیستی از شناسه‌های دسته‌بندی‌ها

    class Config:
        orm_mode = True

# Schema برای ایجاد دسته‌بندی جدید
class CategoryCreate(BaseModel):
    name: str

# Schema برای به‌روزرسانی دسته‌بندی
class CategoryUpdate(BaseModel):
    name: Optional[str]
