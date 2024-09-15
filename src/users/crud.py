from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from .schemas import UserCreate
from ..userProviders.schemas import UserProviderCreate
from ..userProviders.models import UserProvider
from ..ouathProviders.models import OAuthProvider
from ..ouathProviders.schemas import OAuthProviderCreate

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_oauth_provider(db: AsyncSession, provider: OAuthProviderCreate):
    db_provider = OAuthProvider(**provider.model_dump())
    db.add(db_provider)
    await db.commit()
    await db.refresh(db_provider)
    return db_provider

async def link_user_to_provider(db: AsyncSession, user_provider: UserProviderCreate):
    db_user_provider = UserProvider(**user_provider.model_dump())
    db.add(db_user_provider)
    await db.commit()
    await db.refresh(db_user_provider)
    return db_user_provider
    

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
