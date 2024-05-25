import schemas
import uuid
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

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

def transform(db: Session):
    path = "./ExpVinho.csv"
    df = pd.read_csv(path, sep=";", encoding="utf-8")

    df_melted = df.melt(id_vars=["Id", 'País'], var_name='ano', value_name='valor')
    df_final = df_melted.groupby('ano').apply(lambda x: x.groupby(x.columns, axis=1).sum()).reset_index(drop=True)

    df_final.to_csv("ImpVinhos_transformed.csv", index=False)
    df_final['id'] = [uuid.uuid4() for _ in range(len(df_final))]

    for idx, row, in df_final.iterrows():
        db_importing = Exporting(
            id=row['id'],
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
            print(f"Error when inserting {row}: {e}")
        finally:
            db.close()

    return 'Exporting transform done!'
