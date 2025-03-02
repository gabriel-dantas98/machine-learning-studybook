from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from core.config import (
    GRAFANA_OTLP_ENDPOINT,
    GRAFANA_INSTANCE_ID,
    GRAFANA_API_KEY,
    PROJECT_NAME,
)

# Configure OpenTelemetry tracer
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

# Configure OTLP exporter for Grafana Cloud
otlp_endpoint = f"{GRAFANA_OTLP_ENDPOINT}/v1/traces"
otlp_headers = {
    "Authorization": f"Basic {GRAFANA_API_KEY}",
    "X-Scope-OrgID": GRAFANA_INSTANCE_ID,
}

otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, headers=otlp_headers)

tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

resource = Resource.create({"service.name": PROJECT_NAME})
