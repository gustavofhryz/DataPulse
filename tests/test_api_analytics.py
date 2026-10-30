
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.datapulse.api.main import app
from src.datapulse.db.database import Base, get_db
from src.datapulse.db.models import Sale


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestSession = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with TestSession() as session:
        session.add_all(
            [
                Sale(
                    id_venda="V001",
                    data=date(2026, 10, 1),
                    produto="Teclado",
                    quantidade=2,
                    preco_unitario=120.00,
                    faturamento=240.00,
                ),
                Sale(
                    id_venda="V002",
                    data=date(2026, 10, 2),
                    produto="Mouse",
                    quantidade=3,
                    preco_unitario=45.50,
                    faturamento=136.50,
                ),
                Sale(
                    id_venda="V003",
                    data=date(2026, 10, 3),
                    produto="Monitor",
                    quantidade=1,
                    preco_unitario=899.90,
                    faturamento=899.90,
                ),
            ]
        )
        session.commit()

    def override_get_db():
        with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_list_sales_returns_database_records(client):
    response = client.get("/sales")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["id_venda"] == "V003"


def test_summary_calculates_metrics(client):
    response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert response.json() == {
        "total_vendas": 3,
        "faturamento_total": 1276.40,
        "ticket_medio": 425.47,
    }


def test_products_are_ordered_by_revenue(client):
    response = client.get("/analytics/products")

    assert response.status_code == 200

    products = response.json()

    assert [item["produto"] for item in products] == [
        "Monitor",
        "Teclado",
        "Mouse",
    ]
    assert products[0]["faturamento"] == 899.90
