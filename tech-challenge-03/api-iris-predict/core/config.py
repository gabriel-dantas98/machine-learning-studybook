import os

PROJECT_NAME = "API Iris Predict"
MODEL_NAME = 'iris_trained_model.pkl'
TABLE_NAME = os.environ.get("TABLE_NAME") if os.environ.get("TABLE_NAME") else 'iris'
