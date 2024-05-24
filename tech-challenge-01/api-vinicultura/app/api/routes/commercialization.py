from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from services import commercialization
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Commercialization])
def read_all_commercialization(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_commercialization = commercialization.get_all_commercialization(db, skip=skip, limit=limit)
    return all_commercialization
