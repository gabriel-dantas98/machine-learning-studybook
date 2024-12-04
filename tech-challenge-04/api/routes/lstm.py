import torch
from fastapi import APIRouter, Response
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from datasources.yfinance import YahooFinance
from training_models import metrics
from training_models.lstm_finance import LSTMModel
from schemas.LSTMTrainData import LSTMTrainData
from core.observability import logger, tracer
from training_models.metrics import (
    PREDICTION_COUNTER, 
    PREDICTION_LATENCY, 
    TRAINING_COUNTER,
    PREDICTION_ERROR_COUNTER
)

router = APIRouter()

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.post("/predict")
def predict(symbol: str):
    with tracer.start_as_current_span("price_prediction"):
        with PREDICTION_LATENCY.time():
            logger.info(f"Receiving prediction request for {symbol}.")
            try:
                # Get more historical data for prediction
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                yahoo_finance = YahooFinance()
                df = yahoo_finance.collect_data(symbol, start_date, end_date)
                
                if len(df) < 4:  # Minimum required data points for 3-step prediction
                    logger.error(f"Insufficient data points. Found {len(df)}, need at least 4.")
                    PREDICTION_ERROR_COUNTER.inc()
                    return {"error": "Insufficient data points for prediction."}, 400
                    
                logger.info(f"Data collected: {len(df)} records found.")
                logger.info(f"Predicting price for {symbol} using data from {start_date} to {end_date}")

                model = LSTMModel()
                scaled_data, scaler = model.preprocess_data(df)
                x, _ = model.create_dataset(scaled_data, steps=3)
                
                if len(x) == 0:
                    logger.error("No valid sequences could be created from the data.")
                    PREDICTION_ERROR_COUNTER.inc()
                    return {"error": "Insufficient data for prediction sequence."}, 400
                
                x_tensor = torch.FloatTensor(x).reshape(-1, 3, 1)
                
                loaded_model = LSTMModel()
                loaded_model.load_state_dict(torch.load(f'lstm_model_{symbol}.pth'))
                loaded_model.eval()
                
                with torch.no_grad():
                    prediction = loaded_model(x_tensor)
                
                original_prediction = scaler.inverse_transform(prediction.numpy())
                
                logger.info("Prediction completed successfully.")
                PREDICTION_COUNTER.inc()
                return {"prediction": original_prediction.tolist()[0]}

            except FileNotFoundError:
                logger.error("Model file not found.")
                PREDICTION_ERROR_COUNTER.inc()
                return {"error": "Model file not found."}, 500

            except (RuntimeError, ValueError) as e:
                logger.error(f"Error loading model: {e}")
                PREDICTION_ERROR_COUNTER.inc()
                return {"error": "Error loading model. Check file compatibility or integrity."}, 500

            except Exception as e:
                logger.error(f"Error making prediction: {e}")
                PREDICTION_ERROR_COUNTER.inc()
                return {"error": "Error making prediction."}, 500

@router.post("/train")
def train(training_data: LSTMTrainData):
  yfinance = YahooFinance()

  symbol = training_data.symbol

  end_date = datetime.now().strftime('%Y-%m-%d')
  start_date = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')

  df = yfinance.collect_data(symbol, start_date, end_date)

  logger.info(f"Data collected: {len(df)} records found.")

  model = LSTMModel() 
  scaled_data, scaler = model.preprocess_data(df)
  x, y = model.create_dataset(scaled_data)

  x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
  x_train = torch.tensor(x_train, dtype=torch.float32).reshape(x_train.shape[0], x_train.shape[1], 1)
  y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)
  x_val = torch.tensor(x_val, dtype=torch.float32).reshape(x_val.shape[0], x_val.shape[1], 1)
  y_val = torch.tensor(y_val, dtype=torch.float32).reshape(-1, 1)

  model.train_model(x_train, y_train, x_val, y_val, run_name=f"Model_Training_{symbol}")
  mae, rmse = metrics.evaluate_model(model, x_val, y_val)

  torch.save(model.state_dict(), f'lstm_model_{symbol}.pth')
  logger.info(f"Model for {symbol} trained and saved successfully.")

  return {"message": f"Model for {symbol} trained successfully"}
