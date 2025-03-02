import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector

from core.config import TABLE_NAME

CONNECTION_CLOUD_SQL = sqlalchemy.engine.url.URL.create(
    drivername="postgresql+pg8000",
    username="datathon-globo-db",
    password=os.environ.get("DB_PASSWORD"),
    database="datathon",
    query={"host": "/cloudsql/gabsdevops:us-central1:datathon-globo-db"},
)
SQLALCHEMY_DATABASE_URL = (
    CONNECTION_CLOUD_SQL
    if os.environ.get("DB_URL")
    else f"postgresql://datathon:datathon@localhost:6025/{TABLE_NAME}"
)

print("DB_URL LOADED", SQLALCHEMY_DATABASE_URL)
connector = Connector()

def getconn():
    return connector.connect(
        "gabsdevops:us-central1:datathon-globo-db",  # Nome da conexão da instância
        "pg8000",
        user="datathon-globo-db",
        password=os.environ.get("DB_PASSWORD"),
        db="datathon"
    )

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    db = SessionLocal()
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    try:
        yield db
    finally:
        db.close()
