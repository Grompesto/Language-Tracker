from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated, Optional
from config import settings
from starlette import status
from sqlalchemy import func
from models import Word,User
from schemas import WordCreate,UserCreate, UserPublic, Token
from sqlalchemy.orm import Session
from database import get_db,get_user,create_user
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
import random


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="words/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise cred_exc
    return user


### Endpoints ###

@router.post("/register", status_code=201,summary="Create a new user")
def register_user(body: UserCreate, db:Session = Depends(get_db)):
    hashed = hash_password(body.password)
    create_user(username=body.username, hashed_password=hashed, db=db, full_name=body.full_name or "")
    return {"message": "User registered successfully"}

@router.post("/login",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserPublic, summary="Get my profile (protected)")
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.delete("/me")
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(Word).filter(Word.user_id == current_user.id).delete()

    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}

# Create word
@router.post("")
async def create_word(word: WordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Word).filter(func.lower(Word.name) == word.name.lower(), Word.user_id == current_user.id).filter():
        raise HTTPException(status_code=400, detail="Word already exists")

    # Create a new word
    new_word = Word(**word.dict(), user_id = current_user.id)
    
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word

# Delete word
@router.delete("/{word_id}")
async def delete_words(word_id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist")

    db.delete(db_word)
    db.commit()
    return {"message": "Word deleted"}

# Update word
@router.put("/{word_id}")
async def update_word(word_id: int, word:WordCreate, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist")
    for field,value in word.dict(exclude={"review_count","interval"}).items():
        setattr(db_word, field, value)

    db.commit()
    db.refresh(db_word)
    return {"message": "Word updated"}

# Quiz
@router.get("/quiz")
async def quiz_words(db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_words = db.query(Word).filter(Word.user_id == current_user.id).all()
    if not db_words:
        raise HTTPException(status_code=404, detail="No words inside database")

    lowest = min(w.review_count for w in db_words)
    candidates = [w for w in db_words if w.review_count == lowest]
    return random.choice(candidates)


@router.post("/{word_id}/review")
async def review_words(
        word_id: int,
        remembered: bool,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word does not exist in your vocabulary")

    if remembered:
        db_word.review_count += 1
        db_word.interval = max(1, round(db_word.interval * 2.0))
    else:
        db_word.review_count = max(0, db_word.review_count - 1)
        db_word.interval = max(1, round(db_word.interval * 0.5))

    db.commit()
    db.refresh(db_word)
    return {"message": "Word reviewed successfully"}


#Get word
@router.get("")
async def get_words(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Word).filter(Word.user_id == current_user.id).all()