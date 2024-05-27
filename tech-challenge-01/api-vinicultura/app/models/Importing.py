from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Importing(Base):
  __tablename__ = "importing"
  
  id = Column(Integer, primary_key=True, index=True)
  country = Column(String)
  year = Column(String)
  value = Column(Float)
