import schemas
from sqlalchemy.orm import Session
from models.Processing import Processing

def get_processing(db: Session, processing_id: int):
    return db.query(Processing).filter(Processing.id == processing_id).first()

def get_all_processing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Processing).offset(skip).limit(limit).all()

def create_processing(db: Session, processing: schemas.ProcessingCreate):
    db_processing = Processing(**processing.model_dump())
    db.add(db_processing)
    db.commit()
    db.refresh(db_processing)
    return db_processing
