import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
from sklearn.preprocessing import MinMaxScaler
from core.config import MLFLOW_SERVER_URL

from core.observability import logger, tracer
mlflow.set_tracking_uri(MLFLOW_SERVER_URL)

class LSTMModel(nn.Module):
  def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
      super(LSTMModel, self).__init__()
      self.hidden_layer_size = hidden_layer_size
      self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
      self.linear = nn.Linear(hidden_layer_size, output_size)

  def forward(self, input_sequence):
      lstm_output, _ = self.lstm(input_sequence)
      predictions = self.linear(lstm_output[:, -1, :])
      return predictions

  def preprocess_data(self, df):
      with tracer.start_as_current_span("data_preprocessing"):

          logger.info("Starting data preprocessing.")
          df['Close'] = df['Close'].fillna(method='ffill')
          scaler = MinMaxScaler(feature_range=(0, 1))
          scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

          logger.info("Preprocessing completed.")


      return scaled_data, scaler

  def create_dataset(self, data, steps=60):
      with tracer.start_as_current_span("create_dataset"):

          logger.info(f"Creating dataset with {steps} steps for prediction.")
          x, y = [], []

          for i in range(steps, len(data)):
              x.append(data[i-steps:i, 0])
              y.append(data[i, 0])

          logger.info(f"Dataset created with {len(x)} samples.")

      return np.array(x), np.array(y)

  def train_model(self, x_train, y_train, x_val, y_val, epochs=20, run_name="LSTM_Model_Training", patience=5):
      with tracer.start_as_current_span("model_training"):
          mlflow.start_run(run_name=run_name)
          criterion = nn.MSELoss()
          optimizer = optim.Adam(self.parameters(), lr=0.001)
          logger.info(f"Starting model training: {run_name}")
          best_loss = float('inf')
          patience_counter = 0

          for epoch in range(epochs):
              self.train()  # Set model to training mode
              optimizer.zero_grad()
              y_pred = self(x_train)
              loss = criterion(y_pred, y_train)
              loss.backward()
              optimizer.step()
              if epoch % 5 == 0 or epoch == epochs - 1:
                  logger.info(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}')
              mlflow.log_metric("loss", loss.item(), step=epoch)

              # Validation set evaluation
              self.eval()  # Set model to evaluation mode
              with torch.no_grad():
                  y_val_pred = self(x_val)
                  val_loss = criterion(y_val_pred, y_val).item()
                  mlflow.log_metric("val_loss", val_loss, step=epoch)
                  if epoch % 5 == 0 or epoch == epochs - 1:
                      logger.info(f'Epoch {epoch+1}/{epochs}, Validation Loss: {val_loss}')

              # Early stopping check
              if val_loss < best_loss:
                  best_loss = val_loss
                  patience_counter = 0
              else:
                  patience_counter += 1

              if patience_counter >= patience:
                  logger.info("Early stopping activated. Training interrupted.")
                  break

          logger.info("Training completed.")
          mlflow.pytorch.log_model(self, "lstm_model")
          mlflow.end_run()
