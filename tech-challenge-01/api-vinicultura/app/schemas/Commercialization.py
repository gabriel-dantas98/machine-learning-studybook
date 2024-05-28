from pydantic import BaseModel

class CommercializationBase(BaseModel):
  control: str
  product: str
  year: int
  value: float
  category: str

class CommercializationCreate(CommercializationBase):
  control: str
  product: str
  year: int
  value: float
  category: str

class Commercialization(CommercializationBase):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
