import os

PROJECT_NAME = "API PosTech Datathon Globo Recommendation"

# OpenTelemetry Configuration for Local Development
GRAFANA_OTLP_ENDPOINT = os.environ.get(
    "GRAFANA_OTLP_ENDPOINT", "http://localhost:4318"
)  # OTLP HTTP endpoint
GRAFANA_INSTANCE_ID = os.environ.get("GRAFANA_INSTANCE_ID", "local-development")
GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY", "local-key")

# Prometheus Configuration
PROMETHEUS_ENDPOINT = os.environ.get("PROMETHEUS_ENDPOINT", "http://localhost:9090")

# Database
TABLE_NAME = (
    os.environ.get("TABLE_NAME") if os.environ.get("TABLE_NAME") else "datathon"
)
