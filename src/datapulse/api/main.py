
from fastapi import FastAPI

from src.datapulse.api.routes import router as data_router

app = FastAPI(
    title="DataPulse API",
    description="API de análise de vendas e indicadores de negócio",
    version="0.2.0",
)


@app.get("/")
def root():
    return {
        "project": "DataPulse",
        "message": "API de análise de dados",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(data_router)
