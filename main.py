from fastapi import FastAPI
from routers import words
app = FastAPI()

app.include_router(words.router, prefix="/words",tags=["Words"])
