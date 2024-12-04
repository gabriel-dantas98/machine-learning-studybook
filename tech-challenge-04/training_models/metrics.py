import numpy as np
import mlflow
from prometheus_client import Counter, Histogram
from core.observability import tracer, logger

# Prometheus metrics
PREDICTION_COUNTER = Counter('lst_predictions_total', 'Total number of predictions made')
PREDICTION_LATENCY = Histogram('lst_prediction_latency_seconds', 'Time spent processing prediction')
TRAINING_COUNTER = Counter('lst_training_total', 'Total number of model training runs')
MODEL_ERROR_COUNTER = Counter('lst_model_errors_total', 'Total number of model errors')
PREDICTION_ERROR_COUNTER = Counter('lst_prediction_errors_total', 'Total number of prediction errors')

def evaluate_model(model, x, y):
    with tracer.start_as_current_span("model_evaluation") as span:
        try:
            model.eval()
            logger.info("Starting model evaluation.")
            y_pred = model(x).detach().numpy()
            mae = np.mean(np.abs(y.numpy() - y_pred))
            rmse = np.sqrt(np.mean(np.square(y.numpy() - y_pred)))
            
            # Log metrics to MLflow
            mlflow.log_metric("MAE", mae)
            mlflow.log_metric("RMSE", rmse)
            
            logger.info(f"Evaluation completed - MAE: {mae}, RMSE: {rmse}")
            
            # Add metrics to span
            span.set_attribute("MAE", mae)
            span.set_attribute("RMSE", rmse)
            
            return mae, rmse
        except Exception as e:
            logger.error(f"Error in model evaluation: {e}")
            MODEL_ERROR_COUNTER.inc()
            span.set_status(Status(StatusCode.ERROR))
            raise
