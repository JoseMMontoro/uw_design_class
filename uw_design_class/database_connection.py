import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from uw_design_class.singleton_logger import SingletonLogger

dotenv.load_dotenv()
logger = SingletonLogger()

DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PWD")
DB_HOST = "50.17.204.48"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "uw_design_blog"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.log("Database engine created.", module="DatabaseConnection")
except OperationalError as e:
    logger.log(f"Error creating database engine: {e}", module="DatabaseConnection")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logger.log("Creating a new database session.", module="DatabaseConnection")
        yield db
    finally:
        logger.log("Closing the database session.", module="DatabaseConnection")
        db.close()