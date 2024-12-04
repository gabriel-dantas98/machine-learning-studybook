FROM python:3.10

WORKDIR /app

COPY . .

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_SERVICE_NAME="API LSTM Finance Predict"

ENV UVICORN_PORT=8080
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry fastapi uvicorn
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# CMD ["fastapi", "run", "main.py", "--port", "10000", "--proxy-headers"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
