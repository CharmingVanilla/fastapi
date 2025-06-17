from code import interact
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer,String,Boolean
from sqlalchemy.sql.expression import null,text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"  
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,
                      server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),
                                       nullable=None)
    owner=relationship("User") #根据foreigner key直接找出两个class之间的关系 不是users
    
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)   
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,
                      server_default=text('now()'))
    is_admin=Column(Boolean,nullable=False, server_default=text('false'))

class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    

class Comment(Base):
    __tablename__="comments"
    comment_id=Column(Integer,nullable=False,primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False)
    content=Column(String,nullable=False)
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    writer_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,
                      server_default=text('now()'))
    
class Favourite(Base):
    __tablename__="favourites"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)