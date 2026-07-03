from sqlalchemy import String,Integer,Column, ForeignKey
from database import Base,engine

# Database Model
class Word(Base):
    __tablename__ = "Words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    name = Column(String(100), nullable=False,unique=True)
    translation = Column(String(100))
    difficulty = Column(String(30))
    review_count = Column(Integer, default = 0)
    interval = Column(Integer, default = 1)

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True, index=True)
    email = Column(String(100),unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

Base.metadata.create_all(engine)