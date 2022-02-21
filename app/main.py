from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

#! python -m uvicorn app.main:app --reload

# create the database if it doesn't already exist
models.Base.metadata.create_all(bind=engine)  # no longer needed with alembic

# initiate api
app = FastAPI()

# we need to provide a list of domains that can talk to our API. can do * but for security reasons its not best.
origins = ["*"]
# middleware is a function that runs before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # (this is where you set what request types the user is allowed to make (eg POST, GET, DELETE, ect))
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

###############################
# * HOME PAGE


@app.get("/")
def root():
    return {"message": "Hello World!"}
