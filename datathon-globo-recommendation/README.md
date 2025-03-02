# Globo Recommendation System - Datathon Challenge

<p align="center">
  <img src="assets/recommendation-system.jpg">
  <p align="center">
  Este projeto foi desenvolvido durante o Datathon da Globo, com foco em sistemas de recomendação. O objetivo é criar um modelo que recomende conteúdos relevantes para usuários da plataforma Globoplay, melhorando a experiência do usuário e aumentando o engajamento.
  </p>
</p>

## Visão Geral do Projeto

O projeto implementa um sistema de recomendação completo para a plataforma Globoplay, utilizando técnicas avançadas de machine learning para analisar o comportamento dos usuários e recomendar conteúdos personalizados. O modelo considera histórico de visualizações, preferências explícitas e implícitas, e contexto do usuário para gerar recomendações precisas.

## Funcionalidades

- Processamento de dados de interação usuário-conteúdo
- Análise de similaridade entre itens e preferências de usuários
- Algoritmos de filtragem colaborativa e baseada em conteúdo
- Modelo híbrido de recomendação com fatores contextuais
- API RESTful para servir recomendações personalizadas
- Dashboard para visualização de métricas de engajamento

## Estrutura do Projeto

- `api/`: Código da API e rotas do serviço de recomendação
- `assets/`: Recursos estáticos do projeto
- `data_processing/`: Scripts para processamento e limpeza dos dados
- `models/`: Implementação dos algoritmos de recomendação
- `evaluation/`: Métricas e ferramentas de avaliação dos modelos
- `notebooks/`: Jupyter notebooks com análises exploratórias
- `config/`: Arquivos de configuração do sistema
- `utils/`: Funções utilitárias e helpers
- `main.py`: Ponto de entrada da aplicação
- `pyproject.toml` e `poetry.lock`: Gerenciamento de dependências

## Tecnologias Utilizadas

- Python 3.10
- PyTorch e TensorFlow para modelos de deep learning
- Surprise e LightFM para algoritmos de recomendação
- FastAPI para a API REST
- Pandas e NumPy para processamento de dados
- Scikit-learn para avaliação e métricas
- Docker para containerização
- MLflow para tracking de experimentos
- PostgreSQL para armazenamento de dados
- Plotly e Streamlit para visualizações

## Configuração e Instalação

1. Clone o repositório

2. Instale as dependências:

```bash
poetry shell
poetry install
```

3. Configure o ambiente:

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Execute a API:

```bash
python main.py
```

## Uso da API

A documentação da API está disponível em http://localhost:8000/docs, onde é possível testar endpoints como:

- `/recommendations/user/{user_id}`: Obtém recomendações personalizadas para um usuário
- `/recommendations/similar/{item_id}`: Encontra itens similares ao informado
- `/feedback`: Recebe feedback sobre recomendações para melhorar o sistema

## Métricas de Avaliação

O sistema é avaliado usando métricas específicas para recomendação:
- Precision@K e Recall@K
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (NDCG)
- Coverage e Diversidade das recomendações
- Taxa de cliques (CTR) em ambiente de produção

## Desafios e Aprendizados

- Tratamento do cold start para novos usuários e conteúdos
- Balanceamento entre exploração e explotação nas recomendações
- Incorporação de contexto (horário, dispositivo, localização) no modelo
- Escalabilidade para milhões de usuários e conteúdos

## Autor

[Gabriel Dantas](https://gdantas.com.br)
