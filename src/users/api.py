import os
import secrets
from datetime import datetime

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse,RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List
from passlib.context import CryptContext


from src.core.database import get_db
from src.users.models import User
from src.core.config import settings
from .jwt import (
    create_refresh_token,
    create_token,
    CREDENTIALS_EXCEPTION,
    decode_token,
    is_email_registered,
)
from src.users.crud import create_user, get_user_by_email, get_all_users
from src.users.schemas import UserCreate, UserInDB,UserResponse,UserLogin
from src.training.load_model import load_trained_model
from src.training.predict import preprocess_image
import torch

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# OAuth configuration
GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception('Missing environment variables')

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'},
)

# Session secret key
SECRET_KEY = settings.secret_key
if not SECRET_KEY:
    raise Exception('Missing SECRET_KEY')

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import secrets
from src.users.models import User
from src.core.config import settings

router = APIRouter()

@router.get('/login')
async def login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state
    redirect_uri = request.url_for('auth_google')  

    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)


# @router.get("/auth")
# async def auth_google(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.google.authorize_access_token(request)
    
#     user_info = token.get('userinfo')

#     if user_info:
#         user_email = user_info.get("email")

#         if user_email and is_email_registered(user_email, db):
#             user = db.query(User).filter(User.email == user_email).first()
#             if not user:
#                 user = User(
#                     name=user_info.get("name"),
#                     email=user_email,
#                     profile_picture=user_info.get("picture")
#                 )
#                 db.add(user)
#                 db.commit()
#                 db.refresh(user)

#             access_token = create_token(user_email)
#             # Create a redirect response to the frontend
#             response = RedirectResponse(url="http://localhost:5173/upload")  
#             response.set_cookie(key="access_token", value=access_token)  
#             return response

#     raise HTTPException(status_code=400, detail="User not found or not registered")

@router.get("/auth")
async def auth_google(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    if user_info:
        user_email = user_info.get("email")

        # Check if the user already exists in the database
        existing_user = db.query(User).filter(User.email == user_email).first()

        if existing_user:
            # User exists, return access token and user info
            return {
                "access_token": create_token(existing_user.email),
                "user": {
                    "id": existing_user.id,
                    "name": existing_user.name,
                    "email": existing_user.email,
                    "profile_picture": existing_user.profile_picture,
                    "created_at": existing_user.created_at,
                    "last_login": existing_user.last_login
                }
            }
        else:
            new_user = User(
                name=user_info.get("name"),
                email=user_email,  
                profile_picture=user_info.get("picture"),
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            access_token = create_token(new_user.email)  

            frontend_redirect_url = f"http://localhost:5173/login?access_token={access_token}&name={new_user.name}&email={new_user.email}&profile_picture={new_user.profile_picture}"
            return RedirectResponse(url=frontend_redirect_url)

    raise HTTPException(status_code=401, detail="User not found or not registered")



@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# @router.post('/refresh')
# async def refresh(request: Request):
#     """Handles token refresh requests."""
#     try:
#         form = await request.json()
#         if form.get('grant_type') == 'refresh_token':
#             token = form.get('refresh_token')
#             payload = decode_token(token)
#             if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
#                 email = payload.get('sub')
#                 if valid_email_from_db(email):
#                     return JSONResponse({'result': True, 'access_token': create_token(email)})

#     except Exception as e:
#         print(f"Error during refresh: {e}")
#         raise CREDENTIALS_EXCEPTION
#     raise CREDENTIALS_EXCEPTION

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_token(db_user.email)
    
    return {
        "access_token": access_token,
        "user": {
            "id": db_user.id,  
            "name": db_user.name,
            "email": db_user.email,
            "profile_picture": db_user.profile_picture,
            "created_at": db_user.created_at,  
            "last_login": db_user.last_login,  
        }
    }

@router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # first check if the user already exists 
    user_exists = db.query(User).filter(User.email == user.email).first()
    
    if user_exists:
        return {"error": "User already exists"}
    
    hashed_password = hash_password(user.password)
    
    db_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password,
        profile_picture=user.profile_picture,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_token(db_user.email)

    return {
        "access_token": access_token,
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "profile_picture": db_user.profile_picture,
            "created_at": db_user.created_at,
            "last_login": db_user.last_login,
        }
    }

    

@router.get("/users/me", response_model=UserInDB)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    email = decode_token(token)  
    db_user = db.query(User).filter(User.email == email).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  
    return users


@router.post("/users", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user."""
    return create_user(db, user)

@router.get("/users/{email}", response_model=UserInDB)
def read_user(email: str, db: Session = Depends(get_db)):
    """Fetches user by email."""
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Load the trained model for digit prediction
model = load_trained_model()

@router.post("/users/predict-digit/")
def predict_digit(file: UploadFile = File(...)):
    """Predicts a digit from the uploaded image."""
    file_location = f"temp/{file.filename}"
    
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        with open(file_location, "wb+") as f:
            f.write(file.file.read())

        image = preprocess_image(file_location)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        image = image.to(device)
        
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)

        return {"predicted_digit": predicted.item()}
    
    except Exception as e:
        print(f"Server error while predicting digit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
