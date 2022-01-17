from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from starlette.status import HTTP_404_NOT_FOUND
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


# create the database if it doesn't already exist
models.Base.metadata.create_all(bind=engine)


#! python -m uvicorn app.main:app --reload


# initiate api
app = FastAPI()


###############################
##### connect to database #####
# Can copy and paste for any project #
###############################
while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)
###############################

app.include_router(post.router)
app.include_router(user.router)


###############################
# * HOME PAGE
@app.get("/")
def root():
    return {"message": "My first API"}
