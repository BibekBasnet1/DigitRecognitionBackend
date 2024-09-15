from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.config import Base


class UserProvider(Base):
    __tablename__ = "user_providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    provider_id = Column(Integer, ForeignKey('oauth_providers.id'), nullable=False)
    provider_user_id = Column(String(255), unique=True, nullable=False)
    access_token = Column(Text)
    refresh_token = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="user_providers")
    provider = relationship("OAuthProvider", back_populates="user_providers")

