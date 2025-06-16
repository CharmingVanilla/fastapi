from email.policy import HTTP
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2

router=APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def votes(vote:schemas.Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #检验一下是否存在这条post 可以进行点赞
    post_query=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    print(post_query)
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post id:{vote.post_id} does not exit! ")
    
    query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=query.first()
    if vote.post_dir==1: #增加like
        if found_vote: #如果在数据库中发现该用户已有对该帖子进行点赞的记录
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user:{current_user.id} has already voted for the post{vote.post_id}")
        else: #没有这条记录的话就自己写进去
            new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"increase vote successfully!!!"}
    else: #取消like
        #数据库中有这条数据
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'there is no voted post{vote.post_id},so u cant cancel!')
        else:
            query.delete(synchronize_session=False)
            db.commit()
            return{"message":"you have delete the vote successfully!"}


