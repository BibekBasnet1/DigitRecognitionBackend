from sqlalchemy import Column, Integer, String,DateTime
from src.core.config import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    profile_picture = Column(String)
    created_at = DateTime()
    last_login = DateTime()







