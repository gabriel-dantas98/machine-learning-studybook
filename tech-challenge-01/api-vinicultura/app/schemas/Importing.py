from pydantic import BaseModel

class ImportingBase(BaseModel):
  id: int
  country: str
  year: str
  value: float

class ImportingCreate(ImportingBase):
  pass

class Importing(ImportingBase):
  id: int
  country: str
  year: str
  value: float
  
  class Config:
    from_attributes = True
