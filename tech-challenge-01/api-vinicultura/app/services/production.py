import schemas
import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 
from models.Production import Production

def get_production(db: Session, production_id: int):
    return db.query(Production).filter(Production.id == production_id).first()

def get_all_production(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Production).offset(skip).limit(limit).all()

def create_production(db: Session, production: schemas.ProductionCreate):
    db_production = Production(**production.model_dump())
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def delete_production(db: Session, production: schemas.Production):
    db.query(Production).filter(Production.id == production.id).delete()
    db.commit()
    return production

def transform(db: Session):
    path = "./datasource/csv/Producao.csv"
    df = pd.read_csv(path, delimiter=";")
    df.head()
    df_melted = df.melt(id_vars=['id', 'produto'], var_name='ano', value_name='valor')

    df_to_transform = df_melted.copy()
    categoria_atual = None
    for idx, row in df_to_transform.iterrows():
        if row['produto'].isupper():
            categoria_atual = row['produto']
        else:
            df_to_transform.loc[idx, 'categoria'] = categoria_atual

    df_final = df_to_transform[df_to_transform['categoria'].notnull()]
    
    for idx, row in df_final.iterrows():
        if row['ano'] == "control":
            continue

        production_data = {
            "product": row['produto'],
            "year": row['ano'],
            "value": row['valor'],
            "category": row['categoria'],
        }

        db_production = Production(**production_data)

        try:
            db.add(db_production)
            db.commit()
            db.refresh(db_production)
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error when inserting {row}: {e}")
        finally:
            db.close()

    logging.info("done importing data for production...")

    return "Transforming production OK!"
