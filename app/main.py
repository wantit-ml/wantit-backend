from typing import Optional

from fastapi import FastAPI

from app.db.db_setup import db
from app.auth import main as auth
from app.user_api import main as user_api
from app.vacancy_api import main as vacancy_api
from app.firm_api import main as company_api
from app.matching_api import main as matching_api

app = FastAPI()


app.include_router(auth.router, tags=["authentication"], prefix="/auth")
app.include_router(user_api.router, tags=["user api"], prefix="/user")
app.include_router(vacancy_api.router, tags=["vacancy api"], prefix="/vacancy")
app.include_router(company_api.router, tags=["company api"], prefix="/company")
app.include_router(matching_api.router, tags=["matching api"], prefix="/matching")


@app.get("/")
async def read_root():
    return {"Hello": "World"}
