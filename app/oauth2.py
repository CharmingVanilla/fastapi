from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import setting

# 1. 用户输入账号密码 => POST /login
# 2. 登录成功，返回 JWT token
# 3. 用户访问受保护接口 => 带上 Authorization: Bearer <token>
# 4. FastAPI 自动调用 get_current_user()
# 5. 验证 token → 获取 user_id → 传给接口函数

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY
#Algorithm
#expiration_time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY =setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_acess_token(data:dict):  #生成一个带有过期时间的 JWT token
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    #jwt包含payload，秘钥和algorithm
    
    return encoded_jwt

def verify_token_data(token:str,credential_exception): #生成一个带有过期时间的 JWT token。
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str=payload.get("user_id")
        #jwt.decode(...) 会校验 token：是否伪造（通过 SECRET_KEY);是否过期（通过 exp）

        if not id:
            raise credential_exception
        token_data=schemas.TokenData(id=str(id))
    except JWTError:
            raise credential_exception
    
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):  #从 token 中获取当前登录用户的身份信息
     credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f'could not validate the credential',
                                        headers={"WWW-Authenticate":"Bearer"})
     
     token=verify_token_data(token,credential_exception)
     user=db.query(models.User).filter(models.User.id==token.id).first() #从数据库中提取用户
     return user
    # 自动从请求头中提取 token；
    # 验证 token 是否合法；
    # 返回用户身份（通常是 user_id）；
    # 如果失败就返回 401 错误。



    