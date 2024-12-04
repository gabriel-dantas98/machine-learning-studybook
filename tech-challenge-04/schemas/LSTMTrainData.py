from pydantic import BaseModel

class LSTMTrainData(BaseModel):
  symbol: str
