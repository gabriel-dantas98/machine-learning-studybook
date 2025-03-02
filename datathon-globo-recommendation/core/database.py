import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import TABLE_NAME

SQLALCHEMY_DATABASE_URL = (
    os.environ.get("DB_URL")
    if os.environ.get("DB_URL")
    else f"postgresql://datathon:datathon@localhost:6025/{TABLE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    db = SessionLocal()
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    try:
        yield db
    finally:
        db.close()
