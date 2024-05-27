from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from core.database import get_database
from services import exporting
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Exporting])
def read_all_exporting(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_exporting = exporting.get_all_exporting(db, skip=skip, limit=limit)
    return all_exporting

@router.get("/{id}", response_model=schemas.Exporting)
def get_by_id(id: int, db: Session = Depends(get_database)):
    export = exporting.get_exporting(db, exporting_id=id)
    
    if not export:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exporting not found"
        )
    
    return export

@router.post("/", response_model=schemas.Exporting)
def create(request: schemas.Exporting, db: Session = Depends(get_database)):
    return exporting.create_exporting(db, exporting=request)

@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_database)):
    if not exporting.get_exporting(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exporting not found"
        )
    exporting.delete_exporting(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/import")
def import_exporting(db: Session = Depends(get_database)) -> Any:
    return exporting.transform(db)
