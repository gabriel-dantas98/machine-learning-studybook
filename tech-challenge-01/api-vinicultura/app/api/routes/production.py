from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from services import production
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Production])
def get_all_productions(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    productions = production.get_all_production(db, skip=skip, limit=limit)
    return productions

@router.get("/{id}", response_model=schemas.Production)
def get_by_id(id: int, db: Session = Depends(get_database)):
    production = production.get_production(db, production_id=id)
    return production

@router.post("/", response_model=schemas.Production)
def create_production(request: schemas.ProcessingCreate, db: Session = Depends(get_database)):
    return production.create_production(db, production=request)

@router.post("/import")
def import_productions(db: Session = Depends(get_database)) -> Any:
    return production.transform(db)
