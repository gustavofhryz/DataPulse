
from fastapi import FastAPI

app = FastAPI(
    title="DataPulse API",
    description="API para processamento e análise de dados.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "DataPulse",
        "version": "0.1.0",
        "message": "API em execução!",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "datapulse-api",
    }
