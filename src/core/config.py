from pydantic_settings import BaseSettings 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Settings(BaseSettings):
    database_url: str  = "postgresql+asyncpg://postgres:root@localhost/digitrecognition"

    class Config:
        env_file = ".env"

settings = Settings()


