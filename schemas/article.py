from pydantic import BaseModel, validator
from typing import Optional

# مدل پایه برای مقاله (مشترک بین ورودی و خروجی)
class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None

# مدل مخصوص خروجی داده‌های مقاله (شامل id و تصویر)
class Article(ArticleBase):
    id: int
    image: Optional[str] = None

class ImageUpload(BaseModel):
    filename: str
    content_type: str

    @validator('content_type')
    def validate_image_format(cls, v):
        allowed_formats = ["image/jpeg", "image/png"]
        if v not in allowed_formats:
            raise ValueError("فقط فرمت‌های png و jpeg مجاز هستند")
        return v
