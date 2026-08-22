from pydantic import BaseModel
from typing import Optional

# Pydantic Model
class WordCreate(BaseModel):
    name: str
    translation: str
    difficulty: str
    review_count: Optional[int] = 0
    interval: Optional[int] = 1

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    password: str

class UserPublic(BaseModel):
    username: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

