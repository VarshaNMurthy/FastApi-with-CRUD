from fastapi import FastAPI
from blog import models

from .database import engine

from routers import BLOG,USER,authentication

#metadata=MetaData()
app=FastAPI(title="EXAMPLE")

models.Base.metadata.create_all(bind=engine)
app.include_router(USER.router)
app.include_router(authentication.router)
app.include_router(BLOG.router)


'''below commented code is moved to routers folder'''
# @app.post('/create-blog',status_code=status.HTTP_201_CREATED,tags=['BLOG'])
# def create(request:schemas.Blog,db:Session=Depends(get_db)):
#     new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.get('/get-blog',tags=['BLOG'])
# def fetch(db:Session=Depends(get_db)):
#     bloglist=db.query(models.Blog).all()
#     return bloglist


# @app.get('/get-blog-by-id/{id}',tags=['BLOG'],response_model=schemas.ShowBlog)  #response_model=schemas.Blog -> gives details without id or use ShowBlog
# def fetch_by_id(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if blog is None:
#         raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
#     return blog

# @app.put('/update-details/{id}',tags=['BLOG'])
# def update_details(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=404, detail=f'Blog with ID {id} not found')

#     # Update the values of the blog post
#     for key, value in request.model_dump().items():
#         setattr(blog, key, value)

#     db.commit()
#     return 'Update done'

    
# @app.delete('/delete-blog/{id}',tags=['BLOG'])
# def remove(id:int,db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     db.delete(blog)
#     db.commit()
#     return 'Done with deletion'
'''-----------------USER--------------''' 
# pwd=CryptContext(schemes=["bcrypt"],deprecated='auto')
# @app.post('/create-user', status_code=status.HTTP_201_CREATED,tags=['USER'])
# def create_user(request:schemas.User,db:Session=Depends(get_db)):
#     hashedpass=pwd.hash(request.password)
#     new_user = models.User(name=request.name,email=request.email,password=hashedpass)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.post('/create', response_model=schemas.ShowUser,tags=['USER'])
# def create_user(request:schemas.User,db:Session=Depends(get_db)):
#     new_user = models.User(name=request.name,email=request.email)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get('/get-user-by-id/{id}',response_model=schemas.getUser,tags=['USER'])  
# def fetch_user_by_id(id: int, db: Session = Depends(get_db)):
#     u = db.query(models.User).filter(models.User.id == id).first()
#     if u is None:
#         raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    
#     return u

