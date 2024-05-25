from pydantic import BaseModel

class ImportingBase(BaseModel):
  id: str
  country: str
  year: str
  value: float

class ImportingCreate(ImportingBase):
  pass

class Importing(ImportingBase):
  id: str
  country: str
  year: str
  value: float
  
  class Config:
    from_attributes = True
