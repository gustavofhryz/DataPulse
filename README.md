# 📊 DataPulse — Plataforma de Análise de Dados

**Uma plataforma de análise de dados de vendas desenvolvida com Python, Pandas, SQLAlchemy, FastAPI e Streamlit.**

O DataPulse transforma dados brutos de vendas em informações úteis para análise de desempenho, acompanhamento de faturamento e tomada de decisões.

A aplicação integra um pipeline de processamento de dados, persistência em banco de dados, API REST e dashboard interativo, com implantação em ambiente de nuvem.

### 🌐 Acesse o projeto

- **Dashboard:** https://datapulseproject.streamlit.app/
- **API REST:** https://datapulse-api-omhv.onrender.com/
- **Documentação Swagger:** https://datapulse-api-omhv.onrender.com/docs
- **Repositório:** https://github.com/gustavofhryz/DataPulse

---

## 🎯 Objetivo

Desenvolver uma aplicação de análise de dados com arquitetura organizada e componentes integrados, simulando um fluxo de processamento e disponibilização de dados em um ambiente de produção.

O projeto demonstra conhecimentos em engenharia de dados, análise de dados, desenvolvimento de APIs, bancos de dados relacionais, testes automatizados e visualização de informações.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python 3.12 | Linguagem principal |
| Pandas | Limpeza e processamento de dados |
| SQLAlchemy | ORM e integração com bancos de dados |
| SQLite | Persistência no ambiente local |
| PostgreSQL | Banco de dados em produção |
| Neon | PostgreSQL gerenciado na nuvem |
| FastAPI | Desenvolvimento da API REST |
| Streamlit | Dashboard interativo |
| Plotly | Visualização de dados e gráficos |
| Requests | Comunicação HTTP com a API |
| Pytest | Testes automatizados |
| Git e GitHub | Versionamento e publicação |
| Render | Hospedagem da API |
| Streamlit Community Cloud | Hospedagem do dashboard |

## 🏗️ Arquitetura do projeto

O DataPulse utiliza um fluxo integrado de processamento e disponibilização de dados:

```text
              CSV
               |
               v
        PIPELINE DE DADOS
               |
        Python / Pandas
               |
               v
       LIMPEZA E VALIDAÇÃO
               |
               v
        SQLAlchemy / ORM
               |
               v
         BANCO DE DADOS
        SQLite / PostgreSQL
               |
               v
            FastAPI
            REST API
               |
               v
           Streamlit
           Dashboard
               |
               v
      INDICADORES E GRÁFICOS
```

## 📂 Estrutura do projeto

```text
DataPulse/
│
├── data/
│   ├── raw/
│   │   └── vendas.csv
│   │
│   └── processed/
│       └── vendas_limpas.csv
│
├── src/
│   └── datapulse/
│       ├── api/
│       │   ├── main.py
│       │   └── routes.py
│       │
│       ├── dashboard/
│       │   └── app.py
│       │
│       ├── db/
│       │   ├── database.py
│       │   ├── import_sales.py
│       │   ├── models.py
│       │   └── repository.py
│       │
│       └── pipeline/
│           ├── run_pipeline.py
│           └── sales_pipeline.py
│
├── tests/
│   ├── test_api.py
│   ├── test_api_analytics.py
│   ├── test_database.py
│   └── test_sales_pipeline.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

*Observação: `data/processed/vendas_limpas.csv` é gerado pelo pipeline. Arquivos locais e bancos de desenvolvimento são protegidos pelo `.gitignore`.*

## ⚙️ Funcionalidades

### 1. Pipeline de dados

- Leitura de arquivos CSV.
- Processamento e transformação com Pandas.
- Limpeza e validação dos registros.
- Identificação de dados ausentes ou inválidos.
- Validação de quantidades e preços.
- Identificação e tratamento de registros duplicados.
- Cálculo do faturamento por venda.
- Geração de relatório de qualidade dos dados.
- Exportação dos dados processados.

### 2. Banco de dados

- Persistência utilizando SQLAlchemy.
- Suporte a SQLite no ambiente local.
- Integração com PostgreSQL em produção.
- Criação automática da tabela de vendas.
- Importação dos dados processados.
- Prevenção de registros duplicados.

### 3. API REST com FastAPI

A API disponibiliza endpoints para consulta de vendas e indicadores de negócio.

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Informações do projeto |
| GET | `/health` | Verificação de disponibilidade |
| GET | `/sales` | Consulta de vendas |
| GET | `/analytics/summary` | Indicadores gerais |
| GET | `/analytics/products` | Análise por produto |

**Filtros e paginação do endpoint `/sales`:**

- `limit`: quantidade máxima de registros.
- `offset`: deslocamento para paginação.
- `start_date`: data inicial.
- `end_date`: data final.
- `product`: filtro pelo nome do produto.

Exemplo de consulta:

```text
/sales?limit=100&offset=0&product=Mouse
```

### 4. Dashboard interativo

O dashboard apresenta:

- Faturamento total.
- Quantidade de vendas.
- Ticket médio.
- Unidades vendidas.
- Faturamento por produto.
- Evolução diária das vendas.
- Desempenho individual dos produtos.
- Histórico detalhado de vendas.
- Filtros combinados por período e produto.
- Atualização dos dados consultados pela API.

## ☁️ Implantação em produção

O DataPulse está implantado utilizando serviços de nuvem:

| Componente | Serviço |
|---|---|
| API REST | Render |
| Banco de dados | Neon PostgreSQL |
| Dashboard | Streamlit Community Cloud |
| Versionamento | GitHub |

**Aplicação em funcionamento:**

- Dashboard: https://datapulseproject.streamlit.app/
- API: https://datapulse-api-omhv.onrender.com/
- Swagger: https://datapulse-api-omhv.onrender.com/docs

## 💻 Como executar localmente

### 1. Clonar o repositório

```powershell
git clone https://github.com/gustavofhryz/DataPulse.git
cd DataPulse
```

### 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Executar o pipeline

```powershell
python -m src.datapulse.pipeline.run_pipeline
```

O arquivo de entrada utilizado na demonstração está em `data/raw/vendas.csv`.

O resultado processado é gerado em `data/processed/vendas_limpas.csv`.

### 6. Executar a importação para o banco

```powershell
python -m src.datapulse.db.import_sales
```

Sem a variável `DATABASE_URL`, a aplicação utiliza SQLite localmente. Para utilizar PostgreSQL, configure a variável com a URL de conexão do banco.

### 7. Executar a API

```powershell
python -m uvicorn src.datapulse.api.main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

### 8. Executar o dashboard

Em outro terminal, com o ambiente virtual ativado:

```powershell
python -m streamlit run src/datapulse/dashboard/app.py
```

Para conectar o dashboard à API local, configure a variável de ambiente `DATAPULSE_API_URL`:

```powershell
$env:DATAPULSE_API_URL="http://127.0.0.1:8000"
```

Por padrão, o dashboard utiliza a API publicada no Render.

## 🧪 Testes automatizados

O projeto utiliza Pytest para validar os principais componentes.

Execute:

```powershell
python -m pytest -v
```

Os testes abrangem:

- Pipeline de processamento e validação.
- Persistência no banco de dados.
- Endpoints da API.
- Indicadores e consultas analíticas.
- Filtros por data e produto.

**Resultado validado durante o desenvolvimento:** 21 testes aprovados.

## 📈 Evolução do projeto

O DataPulse foi desenvolvido progressivamente:

1. Estruturação do projeto e ambiente Python.
2. Pipeline de processamento com Pandas.
3. Persistência com SQLAlchemy.
4. Desenvolvimento da API REST.
5. Construção do dashboard interativo.
6. Implantação dos serviços em nuvem.
7. Integração com PostgreSQL.
8. Testes automatizados, filtros e refinamento da aplicação.

## 🚀 Possíveis evoluções

- Autenticação e controle de acesso.
- Paginação avançada para grandes volumes de dados.
- Monitoramento e logging.
- Processamento automatizado de novos arquivos.
- Integração com modelos de Machine Learning.
- Previsões de vendas e demanda.
- Agentes de IA para análise automatizada de dados.

## 👨‍💻 Desenvolvedor

**Gustavo Fhryz**

Desenvolvedor com interesse em Inteligência Artificial, automação, análise de dados e desenvolvimento de soluções tecnológicas.

**GitHub:** https://github.com/gustavofhryz

---

**DataPulse — Transformando dados em decisões.**