from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from core.database import get_database
from services import importing
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Importing])
def get_all_importing(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_importing = importing.get_all_importing(db, skip=skip, limit=limit)
    return all_importing

@router.get("/{id}", response_model=schemas.Importing)
def get_by_id(id: int, db: Session = Depends(get_database)):
    imp = importing.get_importing(db, importing_id=id)
    
    if not imp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Importing not found"
        )
    
    return imp

@router.post("/", response_model=schemas.Importing)
def create(request: schemas.Importing, db: Session = Depends(get_database)):
    return importing.create_importing(db, importing=request)

@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_database)):

    if not importing.get_importing(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Importing not found"
        )
    importing.delete_importing(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/import")
def parse_importing(db: Session = Depends(get_database)) -> Any:
    return importing.transform(db)
