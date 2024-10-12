from fastapi import FastAPI
from routers import users, content,article 

app = FastAPI()

app.include_router(users.router,tags=['users'])
app.include_router(content.router,tags=['content'])
app.include_router(article.router,tags=['articles'])

