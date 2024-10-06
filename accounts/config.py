from fastapi import FastAPI
from accounts.routers import users, content 

app = FastAPI()

app.include_router(users.router,tags=['users'])
app.include_router(content.router,tags=['content'])

