from pydantic import BaseModel,Field,EmailStr
from typing import List, Optional

#schema
class Blog(BaseModel):
    title:str=Field(pattern="[A-Z]?[a-z]$")
    body:str=Field(pattern="[A-Z]?[a-z]$")


class User(BaseModel):
    name: str=Field(pattern="[A-Z]?[a-z]$")
    email: EmailStr=Field(pattern="^[a-zA-Z0-9+_.-]+(@gmail.com)$")
    password: str
    
class Update(BaseModel):
    name: str=Field(pattern="[A-Z]?[a-z]$")
    email: EmailStr=Field(pattern="^[a-zA-Z0-9+_.-]+(@gmail.com)$")
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs:List[Blog]
    

class ShowBlog(BaseModel):
    title:str
    body:str 
    creator:ShowUser
    
    
class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]=None 