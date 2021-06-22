from typing import Optional

from fastapi import FastAPI

from app.db.db_setup import db
from app.auth import main as auth
from app.user_api import main as user_api

app = FastAPI()


app.include_router(auth.router, tags=["authentication"], prefix="/auth")
app.include_router(user_api.router, tags=["user api"], prefix="/user")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
