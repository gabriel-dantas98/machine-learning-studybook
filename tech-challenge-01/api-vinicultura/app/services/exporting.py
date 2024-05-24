import schemas
from sqlalchemy.orm import Session
from models.Exporting import Exporting

def get_exporting(db: Session, exporting_id: int):
    return db.query(Exporting).filter(Exporting.id == exporting_id).first()

def get_all_exporting(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Exporting).offset(skip).limit(limit).all()

def create_exporting(db: Session, exporting: schemas.ExportingCreate):
    db_exporting = Exporting(**exporting.model_dump())
    db.add(db_exporting)
    db.commit()
    db.refresh(db_exporting)
    return db_exporting
