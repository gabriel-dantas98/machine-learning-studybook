from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from services import processing
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Processing])
def read_all_processing(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_processing = processing.get_all_processing(db, skip=skip, limit=limit)
    return all_processing

@router.get("/parse")
def parse_processing(db: Session = Depends(get_database)) -> Any:
    return processing.transform(db)
