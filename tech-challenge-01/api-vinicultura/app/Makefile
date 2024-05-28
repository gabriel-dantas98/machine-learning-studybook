run-dev:
	poetry run

run:
	uvicorn main:app --reload

install:
	poetry install

build:
	docker image build . --tag gabsdevops/api-vinicultura

push:
	docker push gabsdevops/api-vinicultura
