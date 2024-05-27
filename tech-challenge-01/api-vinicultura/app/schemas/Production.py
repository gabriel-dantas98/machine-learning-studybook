from pydantic import BaseModel

class ProductionBase(BaseModel):
  id: int
  product: str
  year: int
  value: float
  category: str

class ProductionCreate(ProductionBase):
  pass

class Production(ProductionBase):
  id: int
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
