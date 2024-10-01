from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import accounts.schemas as schemas,accounts.models as models
from accounts.database import engine,SessionLocal
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    db_user =models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()



@app.post("/contents/", response_model=schemas.ContentResponse)
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == content.created_by).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_content = models.Content(title=content.title, description=content.description, created_by=content.created_by)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@app.get("/contents/", response_model=List[schemas.ContentResponse])
def get_contents(db: Session = Depends(get_db)):
    return db.query(models.Content).all()

@app.get("/contents/{content_id}", response_model=schemas.ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@app.put("/contents/{content_id}", response_model=schemas.ContentResponse)
def update_content(content_id: int, content_data: schemas.ContentUpdate, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.title = content_data.title
    content.description = content_data.description
    db.commit()
    db.refresh(content)
    return content

@app.delete("/contents/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return {"detail": "Content deleted successfully"}

































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