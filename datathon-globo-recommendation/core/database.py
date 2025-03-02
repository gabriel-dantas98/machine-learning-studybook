import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import TABLE_NAME

CONNECTION_CLOUD_SQL = sqlalchemy.engine.url.URL.create(
    drivername="postgresql+pg8000",
    username="datathon-globo-db",
    password="datathon-globo-db",
    database="datathon",
    query={"host": "/cloudsql/gabsdevops:us-central1:datathon-globo-db/.s.PGSQL.5432"},
)

SQLALCHEMY_DATABASE_URL = (
    CONNECTION_CLOUD_SQL
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
