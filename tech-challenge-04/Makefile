run-dev:
	poetry run

run:
	export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
	export OTEL_LOGS_EXPORTER=otlp
	export OTEL_SERVICE_NAME="API LSTM Finance Predict"
	uvicorn main:app --reload --port 8080

install:
	poetry install

build:
	docker image build . --tag gabsdevops/api-lts-finance-predict

push:
	docker push gabsdevops/api-lts-finance-predict
