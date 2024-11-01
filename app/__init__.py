from flask import Flask
from dotenv import load_dotenv
from os import getenv
from .models.base_models import BaseModel
from .models.user_models import User
from .models.engine.db_storage import DBStorage
from app.routes import register_routes
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["*"])
app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'default_secret_key')
print("Loaded SECRET_KEY:", app.config['SECRET_KEY'])
storage = DBStorage()
storage.reload()
register_routes(app)
