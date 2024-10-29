from os import environ, path
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    # MYSQL Config
    MYSQL_HOST = environ.get("MYSQL_HOST")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD")
    MYSQL_PORT = int(environ.get("MYSQL_PORT"))
    SQL_PREFIX = environ.get("SQL_PREFIX")

    DB_NAME = environ.get("DB_NAME")

    MYSQL_SQLALCHEMY_DATABASE_URI = f'{SQL_PREFIX}://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{environ.get("DB_NAME")}'

    # Database SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = MYSQL_SQLALCHEMY_DATABASE_URI
