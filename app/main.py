from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from starlette.status import HTTP_404_NOT_FOUND
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# create the database if it doesn't already exist
models.Base.metadata.create_all(bind=engine)


#! python -m uvicorn app.main:app --reload

# initiate api
app = FastAPI()


# you can convert any pydantic model to a dictionary using .dict()
# (BaseModel is a pydantic model (look at imports))


class Post(BaseModel):
    """define a class for a post schema. inhertis from BaseModel class which we import"""
    """We can set fields and their input requirement type"""
    title: str
    content: str
    published: bool = True


###############################
##### connect to database #####
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


# decorator (the path in the brackets denotes the path in the URL we need to go to to access this endpoint)

##################################################################
######################### CRUD operations ######################## ##################################################################
# * HOME PAGE
@app.get("/")
def root():
    return {"message": "My first API"}


# ! TEST ROUTE
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# * GET ALL POSTS
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Data": posts}


# * CREATE A POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
# title string, content string, catagory


# * GET A POST BY ID
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found!')
        # # response and status are imported
    else:
        return {"post_detail": post}


# * DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# * UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


#######################
########################
########################
#########################
#########################
########################

# At first we hard coded data into thie python file in a list.
# Then we stored data in postgres and accessed it using psycopg2 by writing SQL commands directly into the python code.
# Now we are using an ORM model, sqlalchemy. We still have data in postgres, but instaed on writing SQL commands directly into our main pyhton file, we can now use python to perform SQL operations. The ORM model will recieve our python commands and convert them into SQL commands (and will use psycopg2 iteself to communicate with postgres). With this method, we create database.py and models.py scripts.
