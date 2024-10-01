import joblib
import pandas as pd
from core.config import MODEL_NAME
from sklearn.ensemble import RandomForestClassifier

class IrisTrainingModel:
  def __init__(self) -> None:
    self.dataframe = None
    self.trained_model = None
    self.model_name = MODEL_NAME

  def load_model(self):
    try:
      self.trained_model = joblib.load(self.model_name)
    except Exception as e:
      print("Expection", e)
      self.trained_model = self.train_model()
      joblib.dump(self.model, self.model_fname_)

  def train_model(self):
      X = self.dataframe.drop('species', axis=1)
      y = self.dataframe['species']
      rfc = RandomForestClassifier()
      model = rfc.fit(X, y)
      self.trained_model = model
      return model

  def predict_species(self, sepal_length, sepal_width, petal_length, petal_width):
      data_in = [[sepal_length, sepal_width, petal_length, petal_width]]
      prediction = self.trained_model.predict(data_in)
      probability = self.trained_model.predict_proba(data_in).max()
      return prediction[0], probability

  def load_dataset(self):
    df_iris = pd.read_csv("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")
    print(df_iris.head())
    remapping_columns = {
        'sepal length (cm)': 'sepal_length',
        'sepal width (cm)': 'sepal_width',
        'petal length (cm)': 'petal_length',
        'petal width (cm)': 'petal_width'
    }

    df = df_iris.rename(columns=remapping_columns)
    print("Columns:")
    print(df.columns)
    print(df.head())
    self.dataframe = df
    return df
