from fastapi import APIRouter, Depends, HTTPException
from models import Word
from schemas import WordCreate
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()


### Endpoints ###
# Create word
@router.post("")
async def create_word(word: WordCreate, db:Session = Depends(get_db)):
    if db.query(Word).filter(Word.name == word.name).first():
        raise HTTPException(status_code=400, detail="Word already exists")
    # Create a new word
    new_word = Word(**word.dict())
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return {"message": "Word created"}

# Delete word
@router.delete("/{word_id}")
async def delete_words(word_id: int, db:Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist")

    db.delete(db_word)
    db.commit()
    return {"message": "Word deleted"}

# Update word
@router.put("/{word_id}")
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
@router.get("/quiz")
async def quiz_words(db:Session = Depends(get_db)):
    db_words = db.query(Word).all()
    if not db_words:
        raise HTTPException(status_code=404, detail="No words inside database")
    return min(db_words, key=lambda x: x.review_count)

@router.post("/{word_id}/review")
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
@router.get("/{word_id}")
async def get_words(word_id: int, db:Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word