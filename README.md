
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
