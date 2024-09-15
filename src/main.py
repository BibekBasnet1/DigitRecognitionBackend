from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.crud import create_user,get_user_by_email,create_oauth_provider,link_user_to_provider
from src.core.database import get_db
from src.users.schemas import UserCreate,UserInDB
from src.ouathProviders.schemas import OAuthProviderCreate,OAuthProviderInDB
from src.userProviders.schemas import UserProviderCreate,UserProviderInDB
from src.users.api import router as user_router



app = FastAPI()

app.include_router(user_router, prefix="/api")
