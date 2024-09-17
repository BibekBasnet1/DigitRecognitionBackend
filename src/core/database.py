from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from src.core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_= Session,  
    expire_on_commit=False
)

def get_db():
    """Yield a database session."""
    with SessionLocal() as session:
        yield session
