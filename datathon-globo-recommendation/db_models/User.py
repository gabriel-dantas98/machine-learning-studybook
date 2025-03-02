from sqlalchemy import Column, Integer
from pgvector.sqlalchemy import Vector

from core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    read_count = Column(Integer, default=0)
    embedding = Column(Vector(768))  # -768 (BERT-base)
