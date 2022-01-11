from pydantic import BaseModel


# you can convert any pydantic model to a dictionary using .dict()
# (BaseModel is a pydantic model (look at imports))
class Post(BaseModel):
    """define a class for a post schema. inhertis from BaseModel class which we import"""
    """We can set fields and their input requirement type"""
    title: str
    content: str
    published: bool = True
