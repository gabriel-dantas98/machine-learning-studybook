import schemas
from sqlalchemy.orm import Session
from models.Production import Production

def get_production(db: Session, production_id: int):
    return db.query(Production).filter(Production.id == production_id).first()

def get_productions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Production).offset(skip).limit(limit).all()

def create_production(db: Session, production: schemas.ProductionCreate):
    db_production = Production(**production.model_dump())
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production
