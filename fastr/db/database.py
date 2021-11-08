from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastr.config import Settings

from typing import Generator


settings = Settings()

database_url = f"sqlite:///{settings.database_path}"
engine = create_engine(url=database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Connect to the database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
