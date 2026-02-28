import os

# third party libraries
from dotenv import load_dotenv  # library to import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # function that load .env file
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)  # from os standard library getenv() function gets the database url from .env
# creating engine from sqlalchemy
database_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
base = (
    declarative_base()
)  # creates the base class for database and all modules inherit from it


def get_db():
    database = sessionLocal()
    try:
        yield database
    finally:
        database.close()
