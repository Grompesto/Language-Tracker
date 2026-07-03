from pydantic import BaseModel

# Pydantic Model
class WordCreate(BaseModel):
    name: str
    translation: str
    difficulty: str
    review_count: int = 0
    interval: int = 1

class UserCreate(BaseModel):
    email: str
    password: str