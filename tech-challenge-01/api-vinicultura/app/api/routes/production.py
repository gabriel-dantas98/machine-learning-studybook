from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import get_db
from services import production
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Production])
def read_productions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    productions = production.get_productions(db, skip=skip, limit=limit)
    return productions
