from datetime import datetime
import email
from pydantic import BaseModel, EmailStr
# All pydantic models need to extend base model


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# response pydantic model for post
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# response pydantic model for user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# models for logging in...
class UserLogin(BaseModel):
    email: EmailStr
    password: str
