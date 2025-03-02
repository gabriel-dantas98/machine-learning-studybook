run-dev:
	poetry run

run:
	export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
	export OTEL_LOGS_EXPORTER=otlp
	export OTEL_SERVICE_NAME="API PosTech Datathon Globo Recommendation"
	export ENVIRONMENT=development
	export DB_URL="testando"

	uvicorn main:app --reload --port 8080

install:
	poetry install

build:
	docker image build . --tag gabsdevops/api-globo-news-recommendation

push:
	docker push gabsdevops/api-globo-news-recommendation
