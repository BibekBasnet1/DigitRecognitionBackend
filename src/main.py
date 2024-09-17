from fastapi import FastAPI
from src.users.api import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api")


