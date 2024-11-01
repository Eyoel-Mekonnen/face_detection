from os import getenv
from .base_models import BaseModel
from .user_models import User
from .engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
