from .. import models,schemas,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # 查询 Post + 投票数
    posts_with_votes = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.content.contains(search)
    ).limit(limit).offset(skip).all()

    # 拼接评论
    results = []
    for post, vote_count in posts_with_votes:
        comments = db.query(models.Comment).filter(models.Comment.post_id == post.id).all()

        results.append({
            "Post": post,
            "votes": vote_count,
            "comments": comments  # 👈 评论加进来
        })

    return results

# @router.get("/",response_model=List[schemas.PostOut])
# def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
#               limit:int=10,skip:int=0,search:Optional[str]=""):  
#     #db:Session=Depends(get_db) give access to our database
#     # cursor.execute("""SELECT * FROM post""") 
#     # #this is SQL language and we use it to communicate with pgAdmin
#     # posts=cursor.fetchall()
#     #找出符合要求的post
#     #posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
#     #将vote中的like数也join到一起
#     posts_likes=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id)
    
#     posts_add_comment=
#     final_post=posts_add_comment.filter(
#             models.Post.content.contains(search)).limit(limit).offset(skip).all()
#     return final_post

# @app.post('/createposts')
# def create_posts(payload:dict=Body(...)):
#     print(payload)
#     return{"you'v create a new post:",f"title: {payload['title']} content:{payload['content']}"}

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),
                 current_user:int=Depends(oauth2.get_current_user)):
    # 只有登录的用户才能创建帖子，并且你能知道 是哪个用户创建了这个帖子
    # cursor.execute("""INSERT INTO post (title,content,published) VALUES(%s,%s,%s)
    #                RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()  #保存内容到数据库

    # new_post=models.Post(title=post.title,content=post.content,
    #                      published=post.published)
    new_post=models.Post(owner_id=current_user.id,**post.dict())  #自动unpack变成上面的形式
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session=Depends(get_db),
             current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post WHERE id=%s""",(str(id),))
    # post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(
            models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post of {id} was not found")
        # response.status_code=status.HTTP
        # return {"message":f"the post of {id} was not found"}
    return post




@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_one_post(id:int,db:Session=Depends(get_db),
                    current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id=%s RETURNING * """,
    #               (str(id),))
    # delete_post=cursor.fetchone()
    # conn.commit()
    enquiry_post=db.query(models.Post).filter(models.Post.id==id)
    delete_post=enquiry_post.first()

    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post of id{id} does not exist')
    #必须只能删除自己创建的post
    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform request action!')
    # return{"message":"the post has been removed"}
    enquiry_post.delete(synchronize_session=False) #告诉 SQLAlchemy 不需要更新当前 session 中的已加载对象
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title=%s, content=%s,published=%s WHERE id=%s RETURNING *""",
    #                (post.title,post.content,post.published,(str(id),)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    exisiting_post=post_query.first()
    if exisiting_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post of id{id} does not exist')
    #必须只能更新自己创建的post
    if exisiting_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform request action!')
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()