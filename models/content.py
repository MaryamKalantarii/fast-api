from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # فرض بر این است که Base از تنظیمات SQLAlchemy شما آمده است

# جدول میانی برای رابطه‌ی Many-to-Many
posts_category_association = Table(
    'postmodel_category',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# مدل Category
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    
    # رابطه‌ی Many-to-Many با PostModel
    posts = relationship(
        "PostModel",
        secondary=posts_category_association,
        back_populates="categories"
    )

# مدل PostModel
class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_published = Column(Boolean, default=False)

    # رابطه‌ی Many-to-Many با Category
    categories = relationship(
        "Category",
        secondary=posts_category_association,
        back_populates="posts"
    )

    # رابطه با UserModel
    users = relationship("UserModel", back_populates="posts")
