from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import words
from database import Base, engine
import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:63342",
        "http://localhost:63342",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(words.router, prefix="/words",tags=["Words"])
