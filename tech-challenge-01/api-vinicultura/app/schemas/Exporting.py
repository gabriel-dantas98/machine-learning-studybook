from pydantic import BaseModel

class ExportingBase(BaseModel):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str

class ExportingCreate(ExportingBase):
  pass

class Exporting(ExportingBase):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
