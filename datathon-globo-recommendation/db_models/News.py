from sqlalchemy import Column, Integer, String, DateTime, Text, func
from pgvector.sqlalchemy import Vector

from core.database import Base


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    new_hash = Column(String)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    published_at = Column(DateTime, default=func.now())
    popularity = Column(Integer, default=0)
    embedding = Column(Vector(768))
