FROM python:3.9

WORKDIR /app

COPY . .

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry fastapi uvicorn
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["fastapi", "run", "main.py", "--port", "10000", "--proxy-headers"]
