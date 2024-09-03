import os

import dotenv
from sqlalchemy.orm import Session

from uw_design_class.sqlalchemy_database import SQLAlchemyDatabase

dotenv.load_dotenv()

DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PWD")
DB_HOST = "50.17.204.48"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "uw_design_blog"

# Create the database instance
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
database = SQLAlchemyDatabase(db_url)
# Import Base from the database instance
Base = database.Base
# Dependency
def get_db() -> Session:
    db = database.get_session()
    try:
        yield db
    finally:
        database.close_session(db)