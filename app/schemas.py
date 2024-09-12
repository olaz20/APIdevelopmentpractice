from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut (BaseModel):
    id: int
    email: EmailStr  # we are leaving our password so it wont send it back
    
    class Config:   # this will convert it to a regular pydentic model
       from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None
    
class PostBase(BaseModel):  # its a schema model
   title: str
   content: str
   published: bool = True
   
class PostCreate(PostBase):
    pass
class Post(PostBase):  # inherited from postbase # this helps to define response 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # this will return a pydentic model called userout
    
    class Config:
      from_attributes = True
      
      
class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True
    
class Vote(BaseModel):
    post_id: int 
    dir: int
    @validator('dir')
    def validate_dir(cls, v):
        if v not in (0, 1):
            raise ValueError('dir must be 0 or 1')
        return v