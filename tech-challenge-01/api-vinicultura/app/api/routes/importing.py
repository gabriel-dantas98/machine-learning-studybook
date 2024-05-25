from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from services import importing
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Importing])
def read_all_importing(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_importing = importing.get_all_importing(db, skip=skip, limit=limit)
    return all_importing

@router.get("/parse")
def parse_importing(db: Session = Depends(get_database)) -> Any:
    return importing.transform(db)
