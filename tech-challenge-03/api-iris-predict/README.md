# API de Machine Learning para Íris

Este projeto implementa uma API baseada em FastAPI para prever espécies de flores Íris usando machine learning. A API é construída com FastAPI, Poetry e PostgreSQL, utilizando o conjunto de dados Iris para treinamento e previsões.

## Funcionalidades

- Importar e armazenar o conjunto de dados Iris no PostgreSQL
- Recuperar dados Iris armazenados
- Prever espécies de Íris com base em medições de entrada

## Endpoints da API

- `GET /read-dataset`: Recuperar dados Iris armazenados
- `POST /import-dataset`: Importar conjunto de dados Iris e treinar o modelo
- `POST /predict`: Prever espécie de Íris com base em medições de entrada

## Configuração

1. Clone o repositório
2. Instale as dependências usando Poetry: `poetry shell && poetry install`
3. Configure o banco de dados PostgreSQL
4. Configure a conexão do banco de dados em `core/config.py`
5. Execute a API: `poetry run uvicorn main:app --reload`

## Uso

1. Importe o conjunto de dados usando o endpoint `/import-dataset`
2. Faça previsões usando o endpoint `/predict` com entrada JSON:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## Tecnologias Utilizadas

- FastAPI
- Poetry
- PostgreSQL
- SQLAlchemy
- Scikit-learn

Para mais detalhes, consulte o código-fonte e os comentários em cada arquivo.
