from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from core.database import get_database
from services import processing
import schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Processing])
def get_all_processing(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    all_processing = processing.get_all_processing(db, skip=skip, limit=limit)
    return all_processing

@router.get("/{id}", response_model=schemas.Processing)
def get_by_id(id: int, db: Session = Depends(get_database)):
    proc = processing.get_processing(db, processing_id=id)
    
    if not proc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Processing not found"
        )
    
    return proc

@router.post("/", response_model=schemas.Processing)
def create(request: schemas.ProcessingCreate, db: Session = Depends(get_database)):
    return processing.create_processing(db, processing=request)

@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_database)):
    
        if not processing.get_processing(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Processing not found"
            )
        processing.delete_processing(db, id)
    
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/import")
def import_processing(db: Session = Depends(get_database)) -> Any:
    return processing.transform(db)
