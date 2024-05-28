from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from core.database import get_database
from services import commercialization
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Commercialization])
def get_all_commercialization(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_commercialization = commercialization.get_all_commercialization(db, skip=skip, limit=limit)
    return all_commercialization

@router.get("/{id}", response_model=schemas.Commercialization)
def get_by_id(id: int, db: Session = Depends(get_database)):
    comm = commercialization.get_commercialization(db, commercialization_id=id)
    
    if not comm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commercialization not found"
        )
    
    return comm

@router.post("/", response_model=schemas.Commercialization)
def create(request: schemas.CommercializationCreate, db: Session = Depends(get_database)):
    return commercialization.create_commercialization(db, commercialization=request)

@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_database)):

    if not commercialization.get_commercialization(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commercialization not found"
        )
    commercialization.delete_commercialization(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/import")
def import_commercialization(db: Session = Depends(get_database)) -> Any:
    return commercialization.transform(db)
