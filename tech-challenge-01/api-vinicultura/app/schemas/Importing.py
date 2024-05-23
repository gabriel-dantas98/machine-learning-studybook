from pydantic import BaseModel

class ImportingBase(BaseModel):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str

class ImportingCreate(ImportingBase):
  pass

class Importing(ImportingBase):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
