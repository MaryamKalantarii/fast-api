from fastapi import FastAPI ,Path, Query
from pydantic import BaseModel
app = FastAPI()

# first test
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# path parameter
@app.get("/home/{name}/{age}")
def index(name:str,age:int):
    return {"messege": f"Hello, {name}! Your age is {age}."}

#  Request Body & Path Query
class Profile(BaseModel):
    name : str | None = None
    family: str = Path(min_length=3, max_length=50)
    age: int = Path(gt=10, lt=55)


@app.post("/profile")
def create_profile(profile: Profile , q:int = Query(0,ge = 0 , le =100)):
    return profile.name,q



