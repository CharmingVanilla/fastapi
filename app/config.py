from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config():
# ⚠️ 仅在本地加载 .env 文件
        env_file = ".env" if os.getenv("HEROKU_APP_NAME") is None else None

setting=Settings()
