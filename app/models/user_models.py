from .base_models import BaseModel, Base
from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class User(BaseModel, Base):

    __tablename__ = 'users'
    username = Column(String(128), unique=True, nullable=False)
    password_hashed = Column(String(100), nullable=False)
