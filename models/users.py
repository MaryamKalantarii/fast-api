from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder
import datetime

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    update_date = Column(DateTime)
    contents = relationship("Content", back_populates="created_by_user")

