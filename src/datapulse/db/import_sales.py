
from pathlib import Path

from sqlalchemy import func, select

from src.datapulse.db.database import (
    SessionLocal,
    create_tables,
)
from src.datapulse.db.models import Sale
from src.datapulse.db.repository import import_clean_sales_csv


ROOT_DIR = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT_DIR / "data" / "processed" / "vendas_limpas.csv"


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV não encontrado: {CSV_PATH}\n"
            "Execute primeiro o pipeline de vendas da Etapa 2."
        )

    create_tables()

    with SessionLocal() as session:
        report = import_clean_sales_csv(CSV_PATH, session)

        total_sales = session.scalar(
            select(func.count()).select_from(Sale)
        )

        total_revenue = session.scalar(
            select(func.sum(Sale.faturamento))
        ) or 0.0

    print("\n=== DataPulse | Importação SQL ===")

    for key, value in report.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")

    print(f"Total de vendas no banco: {total_sales}")
    print(f"Faturamento total: R$ {total_revenue:.2f}")
    print(f"Banco utilizado: {ROOT_DIR / 'data' / 'datapulse.db'}")


if __name__ == "__main__":
    main()
