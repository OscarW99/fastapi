from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from starlette.status import HTTP_404_NOT_FOUND
import psycopg2
from psycopg2.extras import RealDictCursor
import time


#! python -m uvicorn app.main:app --reload

# initiate api
app = FastAPI()


# you can convert any pydantic model to a dictionary using .dict()
# (BaseModel is a pydantic model (look at imports))

# set up model for which a post must adhere to


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


# * GET ALL POSTS
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"Data": posts}


# * CREATE A POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # the reason for doing this instead of an fstring is to avoid sql injections
    cursor.execute("INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *;",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# title string, content string, catagory


# * GET A POST BY ID
@app.get("/posts/{id}")
def get_post(id: int):
    # cursor.execute expects a string as first argument and tuple as second argument (hence comma next to id).
    cursor.execute("SELECT * FROM posts WHERE id = %s;", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found!')
        # # response and status are imported
    else:
        return {"post_detail": post}


# * DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# * UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')

    return {"data": updated_post}
