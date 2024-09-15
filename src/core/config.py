import os
from pydantic_settings import BaseSettings 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()


