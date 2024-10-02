# API de Machine Learning para Íris

Este projeto implementa uma API baseada em FastAPI para prever espécies de flores Íris. A API é construída com FastAPI, Poetry e PostgreSQL, utilizando o conjunto de dados Iris para treinamento e previsões.

## Funcionalidades

- Importar e armazenar o conjunto de dados Iris no PostgreSQL
- Recuperar dados Iris armazenados
- Prever espécies de Íris com base em medições de entrada

## Endpoints da API

- `GET /read-dataset`: Recuperar dados Iris armazenados
- `POST /import-dataset`: Importar conjunto de dados Iris e treinar o modelo
- `POST /predict`: Prever espécie de Íris com base em medições de entrada

## Utilização do RandomForestClassifier

O RandomForestClassifier é um modelo de ensemble que combina múltiplas árvores de decisão para fazer previsões. Algumas vantagens deste modelo incluem:

- Alta precisão e robustez contra overfitting
- Capacidade de lidar com dados não-lineares
- Fornece importância de features

O modelo é treinado usando o conjunto de dados Iris e é capaz de prever a espécie de uma flor Íris com base em suas medidas de sépala e pétala.

## Configuração

1. Clone o repositório
2. Instale as dependências usando Poetry: `poetry shell && poetry install`
3. Configure o banco de dados PostgreSQL
4. Configure a conexão do banco de dados em `core/config.py`
5. Execute a API: `poetry run uvicorn main:app --reload`

## Uso

1. Importe o conjunto de dados usando o endpoint `/import-dataset`

```bash
curl -X 'POST' \
  'https://desirable-expression-production.up.railway.app/iris/import-dataset' \
  -H 'accept: application/json' \
  -d ''
```

2. Faça previsões usando o endpoint `/predict` com entrada JSON:

```bash
curl -X POST "https://desirable-expression-production.up.railway.app/iris/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "sepal_length": 5.1,
           "sepal_width": 3.5,
           "petal_length": 1.4,
           "petal_width": 0.2
         }'
```

## Tecnologias Utilizadas

- FastAPI
- Poetry
- PostgreSQL
- SQLAlchemy
- Scikit-learn
- Uvicorn
