from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from services import exporting
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Exporting])
def read_all_exporting(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_exporting = exporting.get_all_exporting(db, skip=skip, limit=limit)
    return all_exporting

@router.get("/parse")
def parse_exporting(db: Session = Depends(get_database)) -> Any:
    return exporting.transform(db)
