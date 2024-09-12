
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from random import randrange
from . import models
from .database import engine
from .routers import post, user, auth, vote

from .config import Settings






#models.Base.metadata.create_all(bind=engine)  #this will create a table within postgres

app = FastAPI()

origins = ["*"] #ths is to specify the domains["https://www.google.com", "https://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        
app.include_router(post.router) 
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}




