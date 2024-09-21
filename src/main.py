from fastapi import FastAPI
from src.users.api import router as user_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

app = FastAPI()

# Define allowed origins
# origins = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080","http://localhost:5173/login"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)


SECRET_KEY = settings.secret_key
if not SECRET_KEY:
    raise Exception("Missing SECRET_KEY")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(user_router, prefix="/api")
