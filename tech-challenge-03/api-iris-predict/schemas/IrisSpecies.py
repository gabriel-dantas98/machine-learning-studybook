from pydantic import BaseModel

class IrisSpeciesBase(BaseModel):
  sepal_length: float
  sepal_width: float
  petal_length: float
  petal_width: float

class IrisSpecies(IrisSpeciesBase):
  id: int

  class Config:
    from_attributes = True
