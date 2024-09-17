from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.future import select
from src.users.models import User
from src.users.schemas import UserCreate

DATABASE_URL = "postgresql://postgres:root@localhost/digitrecognition"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    stmt = select(User).filter(User.email == email)
    result = db.execute(stmt)
    return result.scalars().first()

def get_all_users(db: Session):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

# def main():
#     with SessionLocal() as session:
#         user_create = UserCreate(name="John Doe", email="john.doe@example.com")
#         user = create_user(session, user_create)
#         print(f"Created user: {user}")

#     with SessionLocal() as session:
#         user = get_user_by_email(session, "john.doe@example.com")
#         print(f"Retrieved user: {user}")

#     with SessionLocal() as session:
#         users = get_all_users(session)
#         print(f"All users: {users}")

# if __name__ == "__main__":
#     main()
