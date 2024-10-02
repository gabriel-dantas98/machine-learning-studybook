import schemas
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_database
from db_models.IrisSpecies import IrisSpecies
from training_models.iris_model import IrisTrainingModel
from core.config import TABLE_NAME

router = APIRouter()

@router.get("/read-dataset", response_model=list[schemas.IrisSpecies])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)) -> Any:
    iris_species = db.query(IrisSpecies).offset(skip).limit(limit).all()
    return iris_species

@router.post("/import-dataset")
def import_productions(db: Session = Depends(get_database)) -> Any:
    iris_training_model = IrisTrainingModel()
    dataset = iris_training_model.load_dataset()

    dataset.to_sql(TABLE_NAME, db.connection(), if_exists='replace', index=False)
    iris_training_model.train_model()

    return "Everything going ok!"

@router.post("/predict")
def predict_species(iris: schemas.IrisSpeciesBase):
    input_data = iris.dict()

    iris_training_model = IrisTrainingModel()
    dataset = iris_training_model.load_dataset()
    iris_training_model.train_model()

    prediction, probability = iris_training_model.predict_species(
        input_data['sepal_length'], input_data['sepal_width'], input_data['petal_length'], input_data['petal_width']
    )

    return {
        'prediction': prediction,
        'probability': probability
    }
