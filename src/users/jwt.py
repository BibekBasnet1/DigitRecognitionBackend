import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.users.models import User  
from src.core.config import settings
import logging

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  
SECRET_KEY = settings.secret_key

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_token(email: str):
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(email: str):
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(days=30)  
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logging.error(f"Token decode error: {e}")
        raise CREDENTIALS_EXCEPTION

def is_email_registered(email: str, db: Session) -> bool:
    user = db.query(User).filter(User.email == email).first()
    return user is not None
