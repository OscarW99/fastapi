from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

#! python -m uvicorn app.main:app --reload

# create the database if it doesn't already exist
models.Base.metadata.create_all(bind=engine)

# initiate api
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

###############################
# * HOME PAGE
@app.get("/")
def root():
    return {"message": "My first API"}
