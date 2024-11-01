import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()

class BaseModel:
    
    __abstract__ = True 
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = str(uuid.uuid4())
        created_at = datetime.now()
        updated_at = created_at
    
    def save(self):
        from . import storage
        updated_at = datetime.now()
        self.updated_at = datetime.now()
        print("I am inside here")
        storage.new(self)
        storage.save()
