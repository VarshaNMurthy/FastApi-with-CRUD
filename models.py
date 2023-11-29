from sqlalchemy import Column, ForeignKey,Integer,String
from .database import Base
from sqlalchemy.orm import relationship
class Blog(Base):
    __tablename__="blog"
    
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String(20),nullable=False)
    body=Column(String(50))
    creator=relationship("User",back_populates="blogs")
    user_id=Column(Integer,ForeignKey('users.id'))
    
class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)   
    blogs= relationship("Blog",back_populates="creator")
    