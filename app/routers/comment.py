from email.policy import HTTP

from httpx import get
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, dependencies,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2

router=APIRouter(
    prefix="/comment",
    tags=['Comment']
)

#同一个可以多次进行评论
@router.post('/',status_code=status.HTTP_201_CREATED)
def add_comment(comment:schemas.Comment,db:Session=Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user)):
    #对某条帖子进行评论 记录评论的内容 评论的帖子的id 帖子的owner 和评论人的id
    comment_query=db.query(models.Post).filter(models.Post.id==comment.post_id).first()

    if comment_query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f'we cant found the post with id:{comment.post_id}')
    
    if comment_query: #如果找到了这个帖子
        owner_id=comment_query.owner_id
        new_comment=models.Comment(content=comment.content,post_id=comment.post_id,
                                   owner_id=owner_id,writer_id=current_user.id) 
        #自动分配一个comment_id
        db.add(new_comment)
        db.commit()
        return {"message":f"you have comment successfully!!:{new_comment}"}

        
        
#删除评论
@router.delete('/')
def delete_comment(comment:schemas.Comment,db:Session=Depends(get_db),
                   current_user:int=Depends(oauth2.get_current_user)):
    comment_query=db.query(models.Comment).filter(models.Comment.post_id==comment.post_id,
                                                  models.Comment.content==comment.content)
    to_be_delete=comment_query.first()
    
    if to_be_delete==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"we cant found this comment!!")
    
    if to_be_delete.writer_id==current_user.id or current_user.is_admin: #如果这条评论是本人发送的
        if to_be_delete:
                comment_query.delete(synchronize_session=False)
                db.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'Not authorized to perform request action!')
    

