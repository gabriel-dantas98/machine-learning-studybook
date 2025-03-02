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
  - [Exemplo de Uso (Code Snippets)](#exemplo-de-uso-code-snippets)
    - [Criar uma nova notícia  -H "Content-Type: application/json" \\](#criar-uma-nova-notícia---h-content-type-applicationjson-)
    - [Registrar leiturarme demanda.](#registrar-leiturarme-demanda)
    - [Obter recomendações similares](#obter-recomendações-similares)
  - [Integração Contínua e Deploy](#integração-contínua-e-deploy)
    - [Exemplo de Workflow (GitHub Actions)](#exemplo-de-workflow-github-actions)

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

## Tecnologias e Dependênciasse-cased

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
### Instalar dependências

```bash
make installcalhost:8000/news \
```  -H "Content-Type: application/json" \

Instala as bibliotecas necessárias (dentro do container) para a API.,
xt": "Pesquisadores encontram sinais de água em exoplaneta próximo...",
### Rodar a aplicação

```bash
make run
```
  "id": 1,
Sobe o servidor FastAPI em http://localhost:8000 (pode variar conforme a configuração do seu Docker Compose). "title": "Nova Descoberta Espacial",
y": "ciencia"
## Exemplo de Uso (Code Snippets)

A seguir, alguns exemplos de uso prático dos endpoints via curl.
ocalhost:8000/user \
### Criar uma nova notícia  -H "Content-Type: application/json" \

```bash
curl -X POST http://localhost:8000/news \
  -H "Content-Type: application/json" \
  -d '{  "id": 1,
  "title": "Nova Descoberta Espacial", "name": "Alice"
  "text": "Pesquisadores encontram sinais de água em exoplaneta próximo...",
  "category": "ciencia"
  }'
```://localhost:8000/user/1/read/1
Resposta:
Resposta:

```json  "message": "User 1 read news 1 - profile updated."
}
  "id": 1,
  "title": "Nova Descoberta Espacial",ash
  "category": "ciencia"
} -X GET "http://localhost:8000/recommend/similar/1?limit=3"
```osta (exemplo):

### Criar um novo usuário
  {
```bash   "id": 2,
curl -X POST http://localhost:8000/user \ "title": "Descoberta de Partículas",
  -H "Content-Type: application/json" \y": "ciencia"
  -d '{"name": "Alice"}'
```
"id": 3,
Resposta: "title": "Últimas do Futebol",
y": "esporte"
```json
  "id": 1,
  "name": "Alice"ntegração Contínua e Deploy
}
```
GitHub Actions para integração contínua (build e testes a cada push/PR).
### Registrar leiturarme demanda.

```bash
curl -X POST http://localhost:8000/user/1/read/1
```on: [push, pull_request]

Resposta:jobs:
ld-and-test:
```jsontu-latest
{
  "message": "User 1 read news 1 - profile updated."me: Check out code
}ut@v2
```
-python@v2
### Obter recomendações similares
hon-version: 3.9
```bashncies
curl -X GET "http://localhost:8000/recommend/similar/1?limit=3"
```
ts
Resposta (exemplo):n
ker, é feito o push para o Container Registry e, em seguida, o deploy no Cloud Run:
```json
[gcloud run deploy nome-servico \
  {_IMAGE:tag \
  "id": 2,
  "title": "Descoberta de Partículas",
  "category": "ciencia"
  },s são bem-vindas!
  {
  "id": 3,Abra uma issue com sua sugestão ou bug.
  "title": "Últimas do Futebol",ranch para suas mudanças.
  "category": "esporte"
  }
]ojeto está sob a MIT License. Sinta-se livre para usar, modificar e distribuir.
```
---

## Integração Contínua e Deploy

- GitHub Actions para integração contínua (build e testes a cada push/PR).

- Google Cloud Run para deploy serverless dos contêineres, escalando conforme demanda.Datathon Globo Recommendation` até o final).  

### Exemplo de Workflow (GitHub Actions)

```yaml
name: CI

on: [push, pull_request]

jobs:
  build-and-test:
  runs-on: ubuntu-latest
  steps:
    - name: Check out code
    uses: actions/checkout@v2
    - name: Set up Python
    uses: actions/setup-python@v2
    with:
      python-version: 3.9
    - name: Install dependencies
    run: make install
    - name: Run tests
    run: pytest tests
```
