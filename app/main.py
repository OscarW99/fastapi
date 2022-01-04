from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()

# you can convert any pydantic model to a dictionary using .dict()
# (BaseModel is a pydantic model (look at imports))


class Post(BaseModel):
    """define a class for a post schema. inhertis from BaseModel class which we import"""
    """We can set fields and their input requirement type"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# decorator (the path in the brackets denotes the path in the URL we need to go to to access this endpoint)


my_posts = [{"title": "title of post 1", "content": "content of post1", "id": 1},
            {"title": "title of post2", "content": "content of post2", "id": 2}]


@app.get("/")
def root():  # function
    return {"message": "My first API"}


@app.get("/posts")
def get_posts():
    """will get all posts"""
    return {"Data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    print(post_dict)
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title string, content string, catagory


@app.get("/posts/{id}")
def get_post(id: int):  # the id is being taken from the url curly brackets
    # find_post function is defined below
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found!')
        # # response and status are imported
    else:
        return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index:
        my_posts.pop(index)
        return {'message': 'post successfully deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found with id {id}')

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    print(post_dict)
    return {"data": post_dict}


#######################
########################
########################
#########################
#########################
########################
#########################
########################
    ## Other Functions ##


def find_post(id):  # the int part here is builtin fastapi validation that makes sure the id is converted to an integer
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
