from typing import Optional

from fastapi import FastAPI

from app.db.db_setup import db
from app.auth import main as auth
from app.user_api import main as user_api
from app.vacancy_api import main as vacancy_api

app = FastAPI()


app.include_router(auth.router, tags=["authentication"], prefix="/auth")
app.include_router(user_api.router, tags=["user api"], prefix="/user")
app.include_router(vacancy_api.router, tags=["vacancy api"], prefix="/vacancy")


@app.get("/")
async def read_root():
    return {"Hello": "World"}
