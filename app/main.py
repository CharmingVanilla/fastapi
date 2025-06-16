
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware

#print(setting)
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["http://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #what domain can talk to our api
    allow_credentials=True,
    allow_methods=["*"], #allowed http requests
    allow_headers=["*"], #allowed headers
)


my_posts=[{"title":"my daily update","content":"i worked out today","id":1},
          {"title":"my favourite food","content":"must be malatang","id":2}] 
#假装是一个database

def get_one_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def get_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}





