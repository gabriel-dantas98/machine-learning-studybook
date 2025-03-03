import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector

from core.config import TABLE_NAME

def get_connection():
    connector = Connector()
    return connector.connect(
        instance_connection_string="gabsdevops:us-central1:datathon-globo-db",  # Nome da conexão da instância
        driver="pg8000",
        user="postgres",
        password=os.environ.get("DB_PASSWORD"),
        db="postgres"
    )

if os.environ.get("ENVIRONMENT") == 'production':
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=get_connection,
    )
else:
    engine = create_engine(f"postgresql://datathon:datathon@localhost:6025/{TABLE_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    db = SessionLocal()
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    try:
        yield db
    finally:
        db.close()
