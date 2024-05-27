from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Production(Base):
  __tablename__ = "production"
  
  id = Column(Integer, primary_key=True, index=True)
  product = Column(String)
  year = Column(Integer)
  value = Column(Float)
  category = Column(String)
