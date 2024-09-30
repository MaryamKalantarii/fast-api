from fastapi import FastAPI ,Path, Query,Depends,HTTPException
from sqlalchemy.orm import Session
from accounts.database import engine,SessionLocal
import accounts.schemas as schemas,accounts.models as models
from typing import List
# from pydantic import BaseModel, Field
# from typing import Annotated, Literal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get("/users/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users", response_model=List[schemas.UserBase])  
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()  
    return users































# # first test
# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}

# # Query parameter
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}


# # path parameter
# @app.get("/home/{name}/{age}")
# def index(name:str,age:int):
#     return {"messege": f"Hello, {name}! Your age is {age}."}

# #  Request Body & Path Query
# class Profile(BaseModel):
#     name : str | None = None
#     family: str = Path(min_length=3, max_length=50)
#     age: int = Path(gt=10, lt=55)


# @app.post("/profile")
# def create_profile(profile: Profile , q:int = Query(0,ge = 0 , le =100)):
#     return profile.name,q




# # Query Parameter Models
# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}
#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []


# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query


# # Body - Multiple Parameters
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: str | None = None,
#     item: Item | None = None,
#     ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results




# # Declare Request Example Data
# class Content(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 }
#             ]
#         }
#     }


# @app.put("/test/{item_id}")
# async def update_item(item_id: int, content: Content):
#     results = {"item_id": item_id, "content": content}
#     return results