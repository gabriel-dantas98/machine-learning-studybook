run-dev:
	poetry run

run:
	uvicorn main:app --reload --port 8080

install:
	poetry install

build:
	docker image build . --tag gabsdevops/api-iris-predict

push:
	docker push gabsdevops/api-iris-predict
