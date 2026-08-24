from sqlalchemy import String,Integer,Column,Float,DateTime, ForeignKey
from database import Base
from datetime import datetime, timezone

# Database Model
class Word(Base):
    __tablename__ = "Words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    translation = Column(String(100))
    difficulty = Column(String(30))
    ease_factor = Column(Float, default=2.5)
    next_review = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(100),unique=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)

