
import pandas as pd
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from src.datapulse.db.database import Base
from src.datapulse.db.models import Sale
from src.datapulse.db.repository import import_clean_sales_csv


def test_import_and_prevent_duplicate_imports(tmp_path):
    csv_file = tmp_path / "vendas_limpas.csv"

    df = pd.DataFrame(
        [
            {
                "id_venda": "V001",
                "data": "2026-10-01",
                "produto": "Teclado",
                "quantidade": 2,
                "preco_unitario": 120.00,
                "faturamento": 240.00,
            },
            {
                "id_venda": "V002",
                "data": "2026-10-02",
                "produto": "Mouse",
                "quantidade": 3,
                "preco_unitario": 45.50,
                "faturamento": 136.50,
            },
        ]
    )
    df.to_csv(csv_file, index=False)

    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)

    try:
        with TestSession() as session:
            first = import_clean_sales_csv(csv_file, session)

            assert first["importados"] == 2
            assert session.scalar(
                select(func.count()).select_from(Sale)
            ) == 2

            second = import_clean_sales_csv(csv_file, session)

            assert second["importados"] == 0
            assert second["ja_existentes"] == 2
            assert session.scalar(
                select(func.count()).select_from(Sale)
            ) == 2
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
