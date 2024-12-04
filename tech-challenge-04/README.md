# Stock Price Prediction API using LSTM

Este projeto é parte do Tech Challenge da Fase 4 da pós-graduação, focado em Deep Learning e IA. O objetivo é desenvolver um modelo preditivo utilizando redes neurais LSTM (Long Short-Term Memory) para prever o valor de fechamento de ações na bolsa de valores.

## Visão Geral do Projeto

O projeto implementa uma pipeline completa de machine learning, desde a coleta de dados até o deploy de uma API para previsão de preços de ações. O modelo utiliza redes neurais LSTM para capturar padrões temporais em dados históricos de preços de ações.

## Funcionalidades

- Coleta automática de dados históricos de ações via Yahoo Finance
- Pré-processamento e preparação dos dados para treinamento
- Modelo LSTM para previsão de preços
- API RESTful para servir previsões
- Monitoramento de performance do modelo em produção

## Estrutura do Projeto

- `data/`: Dados históricos e processados
- `models/`: Modelo LSTM treinado
- `src/`: Código fonte do projeto
  - `data_collection/`: Scripts para coleta de dados
  - `preprocessing/`: Funções de pré-processamento
  - `model/`: Implementação do modelo LSTM
  - `api/`: Código da API
- `notebooks/`: Jupyter notebooks com análises e desenvolvimento
- `tests/`: Testes unitários e de integração
- `docker/`: Arquivos Docker para containerização

## Tecnologias Utilizadas

- Python 3.8+
- PyTorch para o modelo LSTM
- FastAPI para a API REST
- Docker para containerização
- yfinance para coleta de dados
- Pandas e NumPy para manipulação de dados
- Scikit-learn para métricas e processamento
- MLflow para gerenciamento de experimentos e modelos

## Configuração e Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente necessárias
4. Execute a API:
```bash
uvicorn src.api.main:app --reload
```

## Uso da API

### Endpoint de Previsão

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "symbol": "AAPL",
           "days": 5
         }'
```

## Métricas de Avaliação

O modelo é avaliado usando as seguintes métricas:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- MAPE (Mean Absolute Percentage Error)

## Monitoramento

O sistema inclui monitoramento de:
- Tempo de resposta da API
- Acurácia das previsões
- Utilização de recursos
- Logs de erros e exceções

## Links

- [Documentação da API](link-para-documentacao)
- [Vídeo de Demonstração](link-para-video)
- [Deploy em Produção](link-para-deploy)

## Autor

[Gabriel Dantas](https://gdantas.com.br)
