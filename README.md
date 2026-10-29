
# DataPulse

Plataforma de análise de dados que transforma arquivos CSV
em indicadores acessíveis por API e dashboard web.

## Objetivo

Construir um pipeline de dados com Python, Pandas e SQL,
uma API com FastAPI e um painel de análise com Streamlit.

## Tecnologias

- Python
- Pandas
- SQLAlchemy
- FastAPI
- Streamlit
- Plotly
- Pytest

## Status

Em desenvolvimento — versão 0.1.0.

## Funcionalidades planejadas

- [ ] Importação de CSV
- [ ] Validação e limpeza de dados
- [ ] Persistência em banco SQL
- [ ] API para consulta dos indicadores
- [ ] Dashboard interativo
- [ ] Testes automatizados
- [ ] Containerização com Docker

## Executar localmente

Crie e ative um ambiente virtual, instale as dependências
e inicie os serviços conforme as instruções do projeto.

### API

```powershell
python -m uvicorn src.datapulse.api.main:app --reload
```

Documentação interativa:
http://127.0.0.1:8000/docs

### Dashboard

Em outro terminal, com o ambiente virtual ativado:

```powershell
python -m streamlit run src/datapulse/dashboard/app.py
```

## Licença

A definir.



## Pipeline de dados

O DataPulse possui um pipeline inicial para processamento
de dados de vendas com Pandas.

### Funcionalidades implementadas

- Leitura de CSV com validação das colunas obrigatórias.
- Conversão de datas e valores numéricos.
- Identificação de campos ausentes ou inválidos.
- Validação de quantidades e preços.
- Remoção de vendas duplicadas por identificador.
- Cálculo do faturamento por venda.
- Geração de relatório de qualidade dos dados.
- Exportação do CSV processado.

### Executar o pipeline

```powershell
python -m src.datapulse.pipeline.run_pipeline
```

O arquivo de entrada utilizado na demonstração está em
`data/raw/vendas.csv`.

O resultado é gerado em
`data/processed/vendas_limpas.csv`.

### Executar os testes

```powershell
python -m pytest -v
```


## Persistência SQL

O DataPulse utiliza SQLAlchemy para persistir vendas em um banco SQLite.

### Funcionalidades

- Criação automática da tabela `sales`.
- Identificador de venda como chave primária.
- Importação dos dados processados pelo pipeline Pandas.
- Prevenção de importações duplicadas.
- Consultas SQL para quantidade de vendas e faturamento.

### Executar a importação

```powershell
python -m src.datapulse.db.import_sales
```

O banco local é armazenado em `data/datapulse.db`.
Esse arquivo não deve ser publicado no Git.

### Testes

```powershell
python -m pytest -v
```
