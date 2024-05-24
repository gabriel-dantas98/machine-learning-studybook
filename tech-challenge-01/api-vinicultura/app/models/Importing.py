from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Importing(Base):
  __tablename__ = "importing"
  
  id = Column(Integer, primary_key=True, index=True)
  control = Column(String)
  product = Column(String)
  year = Column(Integer)
  value = Column(Float)
  category = Column(String)
