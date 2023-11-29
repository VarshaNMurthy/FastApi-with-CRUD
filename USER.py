from fastapi import APIRouter,status,HTTPException,Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.database import get_db
from routers import Oauth2
router=APIRouter(tags=['USER'])


pwd=CryptContext(schemes=["bcrypt"],deprecated='auto')
@router.post('/create-user', status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedpass=pwd.hash(request.password)
    existing_user = db.query(models.User).filter(models.User.name == request.name and models.User.email==request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this Details already exists")
    new_user = models.User(name=request.name,email=request.email,password=hashedpass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.post('/create', response_model=schemas.ShowUser,tags=['USER'])
# def create_user(request:schemas.User,db:Session=Depends(get_db)):
#     new_user = models.User(name=request.name,email=request.email)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


@router.get('/get-user-by-id/{id}',response_model=schemas.ShowUser)  
def fetch_user_by_id(id: int, db: Session = Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    u = db.query(models.User).filter(models.User.id == id).first()
    if u is None:
        raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    return u

@router.put('/update-user/{id}',response_model=schemas.ShowUser,)
def Update_user(id:int,request:schemas.Update,db:Session=Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    person = db.query(models.User).filter(models.User.id == id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f'User with ID {id} not found')

    # Update the values of the blog post
    for key, value in request.model_dump().items():
        setattr(person, key, value)

    db.commit()
    return 'Update done'
    
    
@router.delete('/delete-user/{id}',)
def destroy_user(id:int,db: Session = Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    deleted = db.query(models.User).filter(models.User.id == id).first()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with the ID {id} does not exists")
    db.delete(deleted)
    db.commit()
    return 'Done with deletion'