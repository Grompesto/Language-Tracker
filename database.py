from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

from sqlalchemy.sql.functions import user

from fastapi import HTTPException
from config import settings

# Database setup
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(username: str, db:Session):
    from models import User
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user

def create_user(username: str, hashed_password: str, db:Session, full_name: Optional[str] = None):
    from models import User
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    # Create a new user
    new_user = User(username=username,hashed_password=hashed_password,full_name=full_name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user