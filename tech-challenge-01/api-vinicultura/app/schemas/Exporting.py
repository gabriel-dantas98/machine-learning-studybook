from pydantic import BaseModel

class ExportingBase(BaseModel):
  id: str
  country: str
  year: str
  value: float

class ExportingCreate(ExportingBase):
  pass

class Exporting(ExportingBase):
  id: str
  country: str
  year: str
  value: float
  
  class Config:
    from_attributes = True
