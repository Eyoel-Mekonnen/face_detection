from os import getenv

DB_USER = getenv("FRAS_MYSQL_USER")
DB_PASSWORD = getenv("FRAS_MYSQL_PWD")
DB_HOST = getenv("FRAS_MYSQL_HOST")
DB_NAME = getenv("FRAS_MYSQL_DB")

"""
getenv("FRAS_MYSQL_USER")
getenv("FRAS_MYSQL_PWD")
getenv("FRAS_MYSQL_HOST")
getenv("FRAS_MYSQL_DB")
"""


class Config:

    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

