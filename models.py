from sqlalchemy import String,Integer,Column
from database import Base,engine

# Database Model
class Word(Base):
    __tablename__ = "Words"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False,unique=True)
    translation = Column(String(100))
    difficulty = Column(String(30))
    review_count = Column(Integer, default = 0)
    interval = Column(Integer, default = 1)

Base.metadata.create_all(engine)