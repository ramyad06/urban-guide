from fastapi import FastAPI

from app.database import init_db
from app.routes.urls import router

app = FastAPI(title="ShotMe")

init_db()

app.include_router(router)
