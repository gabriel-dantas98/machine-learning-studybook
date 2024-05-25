from pydantic import BaseModel

class ProcessingBase(BaseModel):
  id: str
  control: str
  product: str
  year: int
  value: float
  category: str

class ProcessingCreate(ProcessingBase):
  pass

class Processing(ProcessingBase):
  id: str
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    from_attributes = True
