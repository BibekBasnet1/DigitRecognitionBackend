from pydantic_settings import BaseSettings 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Settings(BaseSettings):
    database_url: str  = "postgresql+asyncpg://postgres:root@localhost/digitrecognition"
    google_client_id: str
    google_client_secret: str
    secret_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"   


settings = Settings()


