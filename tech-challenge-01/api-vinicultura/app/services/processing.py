import schemas
import uuid
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 
from utils import data_format

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

def delete_processing(db: Session, processing: schemas.Processing):
    db.query(Processing).filter(Processing.id == processing.id).delete()
    db.commit()
    return processing

def transform(db: Session):
    path = "ProcessaViniferas.csv"

    df = pd.read_csv(path, sep="\t", encoding="utf-8")
    df_melted = df.melt(id_vars=['id', 'control', 'cultivar'], var_name='ano', value_name='valor')
    df_to_transform = df_melted.copy()

    categoria_atual = None
    for idx, row in df_to_transform.iterrows():
        if row['control'].isupper():
            categoria_atual = row['cultivar']
        else:
            df_to_transform.loc[idx, 'categoria'] = categoria_atual

    df_final = df_to_transform[df_to_transform['categoria'].notnull()]
    df_final['product_id'] = [uuid.uuid4() for _ in range(len(df_final))]
    df_final['valor'] = df_final['valor'].apply(data_format.to_integer_or_zero)

    df_final.to_csv("ProcessaViniferas_transformed.csv", index=False)

    for idx, row in df_final.iterrows():
        db_processing = Processing(
            id=row['product_id'],
            year=row['ano'],
            value=row['valor'],
            category=row['categoria'],
            product=row['cultivar'],
            control=row["control"]
        )

        try:
            db.add(db_processing)
            db.commit()
            db.refresh(db_processing)
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error when inserting {row}: {e}")
        finally:
            db.close()

    return "Transforming Processing OK!"
