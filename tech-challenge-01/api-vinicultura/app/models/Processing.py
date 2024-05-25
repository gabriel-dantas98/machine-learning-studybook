from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Processing(Base):
  __tablename__ = "processing"
  
  id = Column(String, primary_key=True, index=True)
  control = Column(String)
  product = Column(String)
  year = Column(Integer)
  value = Column(Float)
  category = Column(String)
