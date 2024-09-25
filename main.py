from fastapi import FastAPI

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