from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import setting

SQLALCHEMY_DATABASE_URL=f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


#dependency use the session to talk with database
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#用sql方法连接到数据库
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',
                            user='postgres',password='lhy20011230',
                            cursor_factory=RealDictCursor)
        
        cursor=conn.cursor()
        # cursor.execute("SET client_encoding TO 'UTF8'")
        print("the database connection is successful!!")
        break
    except Exception as error:
        print("connecting to database is failed!")
        print("Error:",repr(error))
        time.sleep(2)