
from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from blog import models,database,token
from sqlalchemy.orm import Session
from blog.hashing import Hash
from blog.token import create_access_token
router=APIRouter(tags=['LOGIN'])

@router.post('/login')
def create(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first() #user email should be given here as name
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Wrong password")
    #generate JWT token
    
    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

    
    
    