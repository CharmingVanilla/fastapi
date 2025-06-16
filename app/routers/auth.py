from pydantic import BaseModel
from fastapi import APIRouter,Response,status,HTTPException,Depends
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(  
    prefix='/login',
    tags=['authentication']
)


@router.post('/',response_model=schemas.Token) #客户端必须以 username 和 password 字段进行表单格式提交
def User_login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credential.username).first()

    #RequestForm
    #{
    #   "username":"1111"
    #    "password"："2222"
    #}

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'invalid credential')
    
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'invalid credential')
    
    access_token=oauth2.create_acess_token(data={'user_id':user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
                            