from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Exporting(Base):
  __tablename__ = "exporting"
  
  id = Column(Integer, primary_key=True, index=True)
  country = Column(String)
  year = Column(String)
  value = Column(Float)
