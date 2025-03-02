run-dev:
	poetry run

run:
	export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
	export OTEL_LOGS_EXPORTER=otlp
	export OTEL_SERVICE_NAME=""API PosTech Datathon Globo Recommendation"
	uvicorn main:app --reload --port 8080

run:
	uvicorn main:app  --host 0.0.0.0 --port 8080

install:
	poetry install

build:
	docker image build . --tag gabsdevops/api-globo-news-recommendation

push:
	docker push gabsdevops/api-globo-news-recommendation
