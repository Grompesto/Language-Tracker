from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


# Database setup
engine = create_engine("sqlite:///words.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
