from pydantic import BaseModel

class CommercializationBase(BaseModel):
  id: str
  control: str
  product: str
  year: int
  value: float
  category: str

class CommercializationCreate(CommercializationBase):
  pass

class Commercialization(CommercializationBase):
  id: str
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
