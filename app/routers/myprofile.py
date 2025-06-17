from sqlalchemy.orm import Session
from fastapi import Response, dependencies,status,HTTPException,Depends,APIRouter

from app.database import get_db
from app.routers import vote
from .. import models,schemas,utils,oauth2

router=APIRouter(
    prefix="/me/profile",
    tags=['myprofile']
)

@router.get('/')
def get_my_profile(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    fav_post_ids = [f.post_id for f in db.query(models.Favourite).filter(models.Favourite.user_id==current_user.id).all()]
    favorites = db.query(models.Post).filter(models.Post.id.in_(fav_post_ids)).all()

    vote_post_ids = [f.post_id for f in db.query(models.Vote).filter(models.Vote.user_id==current_user.id).all()]
    votes = db.query(models.Post).filter(models.Post.id.in_(vote_post_ids)).all()
    posts= db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    comments=db.query(models.Comment).filter(models.Comment.writer_id==current_user.id).all()
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "is_admin": current_user.is_admin,
        "posts": posts,
        "favorites": favorites,
        "votes": votes,
        "comments":comments
    }