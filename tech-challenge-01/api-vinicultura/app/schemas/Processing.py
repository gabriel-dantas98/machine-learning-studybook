from pydantic import BaseModel

class ProcessingBase(BaseModel):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str

class ProcessingCreate(ProcessingBase):
  pass

class Processing(ProcessingBase):
  id: int
  control: str
  product: str
  year: int
  value: float
  category: str
  
  class Config:
    orm_mode = True
