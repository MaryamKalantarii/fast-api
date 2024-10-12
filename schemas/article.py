from pydantic import BaseModel
from typing import Optional
from fastapi import Path
# مدل پایه برای مقاله (مشترک بین ورودی و خروجی)
class ArticleBase(BaseModel):
    title: str = Path(min_length=3, max_length=50)
    description: Optional[str] = None

# مدل مخصوص ایجاد مقاله
class ArticleCreate(ArticleBase):
    pass

# مدل مخصوص خروجی داده‌های مقاله (شامل id و تصویر)
class Article(ArticleBase):
    id: int
    image: Optional[str] = None

   