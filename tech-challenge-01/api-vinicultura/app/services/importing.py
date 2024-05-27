import schemas
import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

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

def delete_importing(db: Session, importing: schemas.Importing):
    db.query(Importing).filter(Importing.id == importing.id).delete()
    db.commit()
    return importing

def transform(db: Session):
    path = "./ImpVinhos.csv"

    df = pd.read_csv(path, sep=";", encoding="utf-8")
    year_columns = [col for col in df.columns if col.isdigit()]

    df_melted = df.melt(id_vars=["Id", 'País'], var_name='ano', value_name='valor')
    df_final = df_melted.groupby('ano').apply(lambda x: x.groupby(x.columns, axis=1).sum()).reset_index(drop=True)

    df_final.to_csv("ImpVinhos_transformed.csv", index=False)

    for idx, row, in df_final.iterrows():
        db_importing = Importing(
            year=row['ano'],
            value=row['valor'],
            country=row['País']
        )

        try:
            db.add(db_importing)
            db.commit()
            db.refresh(db_importing)
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error when inserting {row}: {e}")
        finally:
            db.close()

    return "Transforming Imp OK!"
