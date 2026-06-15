from fastapi import FastAPI, HTTPException,Depends

from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import String,Integer,Column,create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


# Database setup
engine = create_engine("sqlite:///words.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

# Pydantic Model
class WordCreate(BaseModel):
    name: str
    translation: str
    difficulty: str
    review_count: int = 0
    interval: int = 1


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

### Endpoints ###

# Create word
@app.post("/words")
async def create_word(word: WordCreate, db:Session = Depends(get_db)):
    if db.query(Word).filter(Word.name == word.name).first():
        raise HTTPException(status_code=404, detail="Word already exists")
    # Create a new word
    new_word = Word(name=word.name)
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return {"message": "Word created"}

# Delete word
@app.delete("/words/{word_id}")
async def delete_words(word_id: int, db:Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist")

    db.delete(db_word)
    db.commit()
    return {"message": "Word deleted"}

# Update word
@app.put("/words/{word_id}")
async def update_word(word_id: int, word:WordCreate, db:Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist")
    for field,value in word.dict().items():
        setattr(db_word, field, value)

    db.commit()
    db.refresh(db_word)
    return {"message": "Word updated"}

# Quiz
@app.get("/words/quiz")
async def quiz_words(db:Session = Depends(get_db)):
    db_words = db.query(Word).all()
    return min(db_words, key=lambda x: x.review_count)

@app.post("/words/{word_id}/review")
async def review_words(word_id: int, remembered: bool, db:Session = Depends(get_db)):
        db_word = db.query(Word).filter(Word.id == word_id).first()
        if not db_word:
            raise HTTPException(status_code=404, detail="Word does not exist")
        if remembered:
            db_word.review_count += 1
            db_word.interval *= 2
            db.commit()
            db.refresh(db_word)
            return {"message": "Word reviewed successfully"}
        else:
            db_word.review_count = 0
            db_word.interval = 1
            db.commit()
            db.refresh(db_word)
            return {"message": "Word wasn't reviewed successfully"}


#Get word
@app.get("/words/{word_id}")
async def get_words(word_id: int, db:Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word