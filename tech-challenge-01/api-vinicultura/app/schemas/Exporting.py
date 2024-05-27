from pydantic import BaseModel

class ExportingBase(BaseModel):
  id: int
  country: str
  year: str
  value: float

class ExportingCreate(ExportingBase):
  pass

class Exporting(ExportingBase):
  id: int
  country: str
  year: str
  value: float
  
  class Config:
    from_attributes = True
