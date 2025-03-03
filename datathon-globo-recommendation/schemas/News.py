from pydantic import BaseModel


class NewsIn(BaseModel):
    text: str
    title: str
