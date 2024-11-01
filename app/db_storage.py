from sqlalchemy import create_engine
from os import getenv
from base_models import BaseModel
from bas_models import Base
from user_models import User
from sqlalchemy.orm import sessionmaker, scoped_sesison
from sqlalchemy import create_engine

class DBStorage:

    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine()

        """
            export HBNB_MYSQL_USER='your_username'
            export HBNB_MYSQL_PWD='your_password'
            export HBNB_MYSQL_HOST='localhost'
            export HBNB_MYSQL_DB='your_database_name'
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("FRAS_MYSQL_USER"),
                                              getenv("FRAS_MYSQL_PWD"),
                                              getenv("FRAS_MYSQL_HOST"),
                                              getenv("FRAS_MYSQL_DB")),
                                      pool_pre_ping=True)
        
    def new(self, obj):

        self.__session.add(obj)

    def save(self):

        self.__session.commit()

    def reload(self):

        Base.metadata.create_all(self.__engine)
        Sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Sess)
        self.__session = Session()

    def close(self):
        
        self.__session.close()
