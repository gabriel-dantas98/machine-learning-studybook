from sqlalchemy import Column, Float, Integer
from core.database import Base

class IrisSpecies(Base):
  __tablename__ = "iris"
  
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  sepal_length = Column(Float)
  sepal_width = Column(Float)
  petal_length = Column(Float)
  petal_width = Column(Float)
