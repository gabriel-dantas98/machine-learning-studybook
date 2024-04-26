from fastapi import FastAPI

from api.main import api_router
from core.config import PROJECT_NAME
from core.database import SessionLocal
app = FastAPI(
    title=PROJECT_NAME,
)

def get_database():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

app.include_router(api_router)
