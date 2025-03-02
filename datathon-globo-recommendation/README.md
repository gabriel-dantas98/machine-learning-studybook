# Datathon Globo Recommendation

Este repositório contém um sistema de recomendação de notícias construído para o desafio **PosTech Datathon Globo**. A solução combina **FastAPI**, **PostgreSQL** (com extensão **pgvector** para embeddings) e **BERT em português** para fornecer recomendações personalizadas de notícias.

---

## Índice
- [Datathon Globo Recommendation](#datathon-globo-recommendation)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
    - [Diagrama Simplificado da Arquitetura](#diagrama-simplificado-da-arquitetura)
    - [Componentes Principais](#componentes-principais)
  - [Arquitetura de Pastas](#arquitetura-de-pastas)
  - [Recursos e EndpointsPOST	/news	Cria nova notícia](#recursos-e-endpointspostnewscria-nova-notícia)
  - [Tecnologias e Dependências](#tecnologias-e-dependências)
  - [Como Executar Localmente](#como-executar-localmente)
    - [Subir serviços com Docker Compose](#subir-serviços-com-docker-compose)

---

## Visão Geral

O objetivo principal é **prever e recomendar notícias** que cada usuário possa ler, considerando:

1. **Cold-start**: novos usuários ou notícias sem histórico.
2. **Recência**: notícias têm prazo de validade curto.
3. **Personalização**: recomendações baseadas no histórico e nos embeddings semânticos (BERT).

### Diagrama Simplificado da Arquitetura

```mermaid
flowchart LR
  subgraph Client
  A[Usuário/Cliente] -->|HTTP Requests| B[API FastAPI]
  end
  subgraph Backend
  B --> D[BERT PT-BR<br>(Embeddings)]
  B --> C[PostgreSQL + pgvector]
  end
  style A fill:#ffc107,stroke:#333,stroke-width:1px
  style B fill:#c8e6c9,stroke:#333,stroke-width:1px
  style C fill:#fff9c4,stroke:#333,stroke-width:1px
  style D fill:#bbdefb,stroke:#333,stroke-width:1px
```

### Componentes Principais

- API FastAPI: expõe rotas para inserir notícias, registrar leituras e gerar recomendações.
- PostgreSQL + pgvector: armazena dados de usuários/notícias, bem como embeddings para busca vetorial.
- BERT em PT-BR: gera embeddings semânticos dos textos das notícias.

## Arquitetura de Pastas

A seguir, a estrutura principal do projeto (omissões de cache e outros detalhes para brevidade):

```bash
.
├── Dockerfile
├── Makefile
├── README.md
├── api
│   ├── main.py                 # Ponto de entrada FastAPI
│   └── routes
│       ├── healthcheck.py
│       ├── links.py
│       ├── news.py
│       ├── raw_data.py
│       ├── recommend.py
│       └── users.py
├── assets
│   └── readme-headline-image.jpg
├── core
│   ├── bert_embeddings.py
│   ├── config.py
│   ├── database.py
│   ├── logging.py
│   ├── observability.py
├── datasources
│   ├── train
│   │   ├── news
│   └── security.py
├── datasourcesacao.csv
│   ├── train
│   │   ├── news
│   │   └── ...
│   └── validacao.csvpy
├── db_models_.py
│   ├── News.py.yml
│   ├── RawData.py
│   ├── User.pyments
│   └── __init__.pyipynb
├── docker-compose.ymllock
├── main.py
├── notebook-experiments
│   └── data_cleaning.ipynb
├── poetry.lock
├── pyproject.tomlnit__.py
├── schemas
│   ├── News.py
│   ├── Users.py
│   └── __init__.pys pontos:**
└── scripts

```api/: contém o arquivo main.py (ponto de entrada do FastAPI) e as rotas em api/routes.
iguração, conexão ao DB, geração de embeddings, etc.
**Principais pontos:**db_models/: definição de modelos (ORM) de banco de dados.

- **api/**: contém o arquivo main.py (ponto de entrada do FastAPI) e as rotas em api/routes.stração do container.
- **core/**: módulos de configuração, conexão ao DB, geração de embeddings, etc.
- **db_models/**: definição de modelos (ORM) de banco de dados.s (news, user, recommend, etc.). Alguns dos endpoints:
- **schemas/**: modelos Pydantic para entrada/saída de dados.
- **docker-compose.yml** e **Dockerfile**: contêm instruções para construção e orquestração do container.o

## Recursos e EndpointsPOST	/news	Cria nova notícia
usuário
A API segue uma estrutura de rotas dividida por recursos (news, user, recommend, etc.). Alguns dos endpoints:tra leitura de notícia pelo usuário
_id}	Recomenda notícias similares ao perfil do user
| Método | Rota | Descrição |r_id}	Recomenda notícias em tendência
|--------|------|-----------|
| GET | /healthcheck/ping | Healthcheck simples |
| POST | /news | Cria nova notícia |
| POST | /user/{user_id}/read/{news_id} | Registra leitura de notícia pelo usuário || POST | /user | Cria novo usuário |
| GET | /recommend/similar/{user_id} | Recomenda notícias similares ao perfil do user |mit=5
| GET | /recommend/trending/{user_id} | Recomenda notícias em tendência |Retorna as top 5 notícias de tecnologia mais similares ao embedding do usuário ID=1.
| GET | /raw_data | Loader de dados brutos (exemplo) |

Exemplo de rota de recomendação (similaridade):

`GET /recommend/similar/1?category=tecnologia&limit=5`FastAPI (Framework Web)
+ pgvector (Banco de dados + extensão para vetores)
Retorna as top 5 notícias de tecnologia mais similares ao embedding do usuário ID=1. (Containerização)

## Tecnologias e Dependências

- Python 3.9+
- FastAPI (Framework Web)
- PostgreSQL + pgvector (Banco de dados + extensão para vetores)
- Docker e Docker Compose (Containerização)Subir serviços com Docker Compose
- Make (Automação de scripts)
- BERT PT-BR: neuralmind/bert-base-portuguese-casede dados PostgreSQL (com pgvector) e os demais serviços.
- SQLAlchemy (ORM)
- PyTorch (execução do modelo BERT)

## Como Executar Localmente
Instala as bibliotecas necessárias (dentro do container) para a API.

### Subir serviços com Docker Compose

```bash
docker-compose up
```Sobe o servidor FastAPI em http://localhost:8000 (pode variar conforme a configuração do seu Docker Compose).

Esse comando inicializa o banco de dados PostgreSQL (com pgvector) e os demais serviços.
A seguir, alguns exemplos de uso prático dos endpoints via curl.
