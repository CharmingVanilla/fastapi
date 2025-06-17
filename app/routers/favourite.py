from sqlalchemy.orm import Session
from fastapi import Response, dependencies,status,HTTPException,Depends,APIRouter

from app.database import get_db
from .. import models,schemas,utils,oauth2

router=APIRouter(
    prefix="/favourites",
    tags=['Favourites']
)

#收藏帖子或者取消收藏帖子
@router.post("/",status_code=status.HTTP_201_CREATED)
def favourite_post(post:schemas.Vote,db:Session=Depends(get_db),
                   current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==post.post_id)
    favourite_post=post_query.first()
    #如果这篇帖子不存在
    if not favourite_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'we cant find the post id:{post.post_id}')
    #如果这篇帖子存在
    #在数据库中寻找是否有这条记录
    query=db.query(models.Favourite).filter(post.post_id==models.Favourite.post_id)
    favourite_query=query.first()
    if post.post_dir:     #我想对他进行收藏
        if favourite_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"the post:{post.post_id} has already been favourited!!")
        else:
            new_fav=models.Favourite(post_id=post.post_id,user_id=current_user.id)
            db.add(new_fav)
            db.commit()
            return {"message":"add to favourite successfully!!!"}
    else: #我想取消收藏
        if favourite_query:
            query.delete(synchronize_session=False)
            db.commit()
            return{"message":"you have delete the favourite successfully!"}
        else:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'there is no favourited post{post.post_id},so u cant cancel!')






    
