from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from uw_design_class.database_interface import DatabaseInterface
from uw_design_class.singleton_logger import SingletonLogger


class SQLAlchemyDatabase(DatabaseInterface):
    def __init__(self, db_url: str):
        self.logger = SingletonLogger()
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self) -> Session:
        self.logger.log("Creating a new database session.", module="DatabaseConnection")
        return self.SessionLocal()

    def close_session(self, db: Session):
        self.logger.log("Closing the database session.", module="DatabaseConnection")
        db.close()
