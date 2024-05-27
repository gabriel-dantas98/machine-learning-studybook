import schemas
import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from models.Commercialization import Commercialization

def get_commercialization(db: Session, commercialization_id: int):
    return db.query(Commercialization).filter(Commercialization.id == commercialization_id).first() is not None

def get_all_commercialization(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Commercialization).offset(skip).limit(limit).all()

def create_commercialization(db: Session, commercialization: schemas.CommercializationCreate):
    db_commercialization = Commercialization(**commercialization.model_dump())
    db.add(db_commercialization)
    db.commit()
    db.refresh(db_commercialization)
    return db_commercialization

def delete_commercialization(db: Session, id: int):
    commercialization = db.query(Commercialization).filter(Commercialization.id == id).first()
    
    if commercialization is not None:
        db.delete(commercialization)
        db.commit()

def transform(db: Session):
    path = "./datasource/csv/Comercio.csv"
    years = [str(year) for year in range(1970, 2023)]
    columns = [*["id", "control", "produto"], *years]

    df = pd.read_csv(path, sep=";", encoding="utf-8", names=columns)
    logging.info("dataframe loaded", df.count)
    df_melted = df.melt(id_vars=['id', 'control', 'produto'], var_name='ano', value_name='valor')
    df_to_transform = df_melted.copy()

    categoria_atual = None
    for idx, row in df_to_transform.iterrows():
        if row['control'].isupper():
            categoria_atual = row['control']
        else:
            df_to_transform.loc[idx, 'categoria'] = categoria_atual

    df_final = df_to_transform[df_to_transform['categoria'].notnull()]

    for idx, row, in df_final.iterrows():
        db_commercialization = Commercialization(
            control=row['id'],
            product=row['control'].strip(),
            year=row['ano'],
            value=row['valor'],
            category=row['categoria']
        )

        try:
            db.add(db_commercialization)
            db.commit()
            db.refresh(db_commercialization)
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error when inserting {row}: {e}")
        finally:
            db.close()

    logging.info("done importing data for commercialization...")

    return "Transforming Comercio OK!"
