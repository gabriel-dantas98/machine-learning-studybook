from sqlalchemy import Column, Float, Integer, String
from ..core.database import Base

class Exporting(Base):
  __tablename__ = "exporting"
  
  id = Column(Integer, primary_key=True, index=True)
  control = Column(String)
  product = Column(String)
  year = Column(Integer)
  value = Column(Float)
  category = Column(String)
