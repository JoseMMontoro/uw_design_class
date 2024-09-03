from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class DatabaseInterface(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        pass
