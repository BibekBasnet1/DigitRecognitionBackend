from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.users.crud import create_user, get_user_by_email,get_all_users
from src.users.schemas import UserCreate, UserInDB

router = APIRouter()

@router.get("/users", response_model=list[UserInDB])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return users
   

# @router.get("/users/", response_model=dict)
# async def list_users(db: AsyncSession = Depends(get_db)):
#     return {"test": "hello world"}

@router.post("/users/", response_model=UserInDB)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/users/{email}", response_model=UserInDB)
async def read_user(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
