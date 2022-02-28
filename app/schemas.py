from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime

# User schema as a response model (in routers/user.py)
class User(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        
# Schema for new user data (in routers/user.py)
class NewUser(BaseModel):
    email: str
    password: str

# Post schema as a response model (in routers/post.py)
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: User
    
    class Config:
        orm_mode = True
      
        
class PostWithVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
    
# Schema for new post data (in routers/post.py)
class NewPost(BaseModel):
    title: str
    content: str
    published: bool = True

# Schemas for Login (auth.py)
# class UserLogin(BaseModel):
#     email: str
#     password: str

# Token schema as a response Model (in auth.py)
class Token(BaseModel):
    access_token: str
    token_type: str

# Token schema used on verified token (in oauth.py)
class TokenData(BaseModel):
    id: Optional[str] = None


# Vote schema
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)