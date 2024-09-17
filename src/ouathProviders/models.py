
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.config import Base

class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String(255), unique=True, nullable=False)
    provider_url = Column(String(255), nullable=False)

    user_providers = relationship("UserProvider", back_populates="provider")





