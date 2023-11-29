import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql+psycopg2://postgres:tiger@localhost/postgres")
Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()