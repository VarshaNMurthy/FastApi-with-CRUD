from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.database import get_db
from routers import Oauth2

router=APIRouter(
    #prefix='/blog',  used for prefixing the path
    tags=['BLOG'])



@router.get('/get-blog')
def fetch(db:Session=Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    bloglist=db.query(models.Blog).all()
    return bloglist

# @router.post('/create-blog',status_code=status.HTTP_201_CREATED,)
# def create(request:schemas.Blog,db:Session=Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
#     existing_blog = db.query(models.Blog).filter(models.Blog.title == request.title).first()
#     if existing_blog:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog with this title already exists")

#     new_blog=models.Blog(title=request.title,body=request.body,user_id=models.Blog.user_id)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog


@router.post('/create-blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(Oauth2.get_current_user)):
    # print(current_user.email)
    c_user_id=db.query(models.User).filter(models.User.email==current_user.email).first()
    cur_user_id=c_user_id.id
    existing_blog = db.query(models.Blog).filter(models.Blog.title == request.title).first()
    if existing_blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog with this title already exists")

    new_blog = models.Blog(title=request.title, body=request.body, user_id=cur_user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.get('/get-blog-by-id/{id}',response_model=schemas.ShowBlog)  #response_model=schemas.Blog -> gives details without id or use ShowBlog
def fetch_by_id(id: int, db: Session = Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    return blog

@router.put('/update-details/{id}')
def update_details(id: int, request: schemas.Blog, db: Session = Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog with ID {id} not found')

    # Update the values of the blog post
    for key, value in request.model_dump().items():
        setattr(blog, key, value)

    db.commit()
    return 'Update done'

    
@router.delete('/delete-blog/{id}')
def remove(id:int,db: Session = Depends(get_db),current_user:schemas.User=Depends(Oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog with the ID {id} does not exists")
    db.delete(blog)
    db.commit()
    return 'Done with deletion'