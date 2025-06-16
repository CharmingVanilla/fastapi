from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_users(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO post (title,content,published) VALUES(%s,%s,%s)
    #                RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()  #保存内容到数据库

    # new_post=models.Post(title=post.title,content=post.content,
    #                      published=post.published)

    ##hash the password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())  #自动unpack变成上面的形式
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post of {id} was not found")
        # response.status_code=status.HTTP
        # return {"message":f"the post of {id} was not found"}
    return user