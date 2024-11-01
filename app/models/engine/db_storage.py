from sqlalchemy import create_engine
from os import getenv
from app.models.base_models import BaseModel
from app.models.base_models import Base
from app.models.user_models import User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

class DBStorage:

    __engine = None
    __session = None

    def __init__(self):

        """
            export HBNB_MYSQL_USER='your_username'
            export HBNB_MYSQL_PWD='your_password'
            export HBNB_MYSQL_HOST='localhost'
            export HBNB_MYSQL_DB='your_database_name'
        """

        """
        getenv("FRAS_MYSQL_USER")
        getenv("FRAS_MYSQL_PWD")
        getenv("FRAS_MYSQL_HOST")
        getenv("FRAS_MYSQL_DB")
        """
        load_dotenv()
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("FRAS_MYSQL_USER"),
                                              getenv("FRAS_MYSQL_PWD"),
                                              getenv("FRAS_MYSQL_HOST"),
                                              getenv("FRAS_MYSQL_DB")),
                                      pool_pre_ping=True)
        #print("DEBUG ENVIRONMENT VARIABLES:")
        #print("MySQL User:", getenv("FRAS_MYSQL_USER"))
        #print("MySQL Password:", getenv("FRAS_MYSQL_PWD"))
        #print("MySQL Host:", getenv("FRAS_MYSQL_HOST"))
        #print("MySQL DB:", getenv("FRAS_MYSQL_DB"))
        
    def new(self, obj):
        #print("I am in new in dbstorage")
        self.__session.add(obj)

    def save(self):
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
        #print("He called me here In commit")

    def reload(self):
        
        #print("I am being loaded")
        Base.metadata.create_all(self.__engine)
        Sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Sess)
        self.__session = Session()
        #print("Session successfully reloaded and configured.")

    def close(self):
        
        self.__session.close()
    
    def authenticate_user(self, username, password):
        user_validation = self.__session.query(User).filter_by(username=username).first()
        #print(user_validation)
        if user_validation and check_password_hash(user_validation.password_hashed, password):
            return True
        else:
            return False
