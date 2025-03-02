FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_SERVICE_NAME="API Globo News Recommendation"
ENV TRANSFORMERS_CACHE=/app/cache

ENV UVICORN_PORT=8080
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry fastapi uvicorn pg8000 prometheus_fastapi_instrumentator
RUN poetry config virtualenvs.create false
RUN poetry install

RUN python -c "from transformers import AutoTokenizer, AutoModel; \
                AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased'); \
                AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')"

RUN tree

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
