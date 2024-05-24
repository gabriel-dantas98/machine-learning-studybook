import schemas
from sqlalchemy.orm import Session
from models.Commercialization import Commercialization

def get_commercialization(db: Session, commercialization_id: int):
    return db.query(Commercialization).filter(Commercialization.id == commercialization_id).first()

def get_all_commercialization(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Commercialization).offset(skip).limit(limit).all()

def create_commercialization(db: Session, commercialization: schemas.CommercializationCreate):
    db_commercialization = Commercialization(**commercialization.model_dump())
    db.add(db_commercialization)
    db.commit()
    db.refresh(db_commercialization)
    return db_commercialization
