import schemas
from sqlalchemy.orm import Session
from models.Importing import Importing

def get_importing(db: Session, importing_id: int):
    return db.query(Importing).filter(Importing.id == importing_id).first()

def get_all_importing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Importing).offset(skip).limit(limit).all()

def create_importing(db: Session, importing: schemas.ImportingCreate):
    db_importing = Importing(**importing.model_dump())
    db.add(db_importing)
    db.commit()
    db.refresh(db_importing)
    return db_importing
