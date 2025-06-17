from ast import Str
from re import S
from secrets import token_bytes
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional
from typing import List

from sqlalchemy import Integer




class PostBase(BaseModel):
    #id:int
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    pass

    # class Config:
    #     from_attributes = True

class PostResponse(PostBase): #传回指令的request model 不返回id和created_time#
    #同样返回用户的数据
    
    id:int
    owner_id:int
    owner:UserResponse

    class Config: ##告诉pydantic model去读取数据即使他不是一个dict
        orm_mode = True

class CommentOut(BaseModel):
    comment_id: int
    content: str
    writer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel): #不从postBase继承 而是从basemodel继承
    Post: PostResponse # 你原来的 Post Pydantic Model
    votes: int  
    comments:List[CommentOut]

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:EmailStr
    password:str
    is_admin:bool=False




class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None 

class Vote(BaseModel):
    post_id:int
    post_dir:int

class Comment(BaseModel):
    post_id:int
    content:str
    # owner_id:int 这个好像可以查出来
    # writer_id:int

