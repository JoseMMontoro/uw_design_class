from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(BaseModel):
    title: str
    content: str
    authorid: int
    publisheddate: Optional[datetime] = None  # Allow None to use the default value
    blogid: Optional[int] = 1  # default main blog  


class Post(PostBase):
    postid: int
    publisheddate: Optional[datetime] = None
    authorid: Optional[int] = None
    blogid: Optional[int] = None

    class Config:
        orm_mode = True
