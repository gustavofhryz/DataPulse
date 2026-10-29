
from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.datapulse.db.models import Sale


def import_clean_sales_csv(
    csv_path: str | Path,
    session: Session,
) -> dict[str, int]:
    """Importa vendas limpas, sem duplicar IDs já armazenados."""
    df = pd.read_csv(csv_path, dtype={"id_venda": "string"})

    required = {
        "id_venda",
        "data",
        "produto",
        "quantidade",
        "preco_unitario",
        "faturamento",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Colunas ausentes no CSV processado: {sorted(missing)}"
        )

    existing_ids = set(session.scalars(select(Sale.id_venda)).all())
    seen_in_file: set[str] = set()

    report = {
        "recebidos": len(df),
        "importados": 0,
        "ja_existentes": 0,
        "duplicados_no_arquivo": 0,
    }

    try:
        for row in df.to_dict(orient="records"):
            sale_id = str(row["id_venda"]).strip()

            if sale_id in seen_in_file:
                report["duplicados_no_arquivo"] += 1
                continue

            seen_in_file.add(sale_id)

            if sale_id in existing_ids:
                report["ja_existentes"] += 1
                continue

            sale = Sale(
                id_venda=sale_id,
                data=pd.to_datetime(row["data"]).date(),
                produto=str(row["produto"]).strip(),
                quantidade=int(row["quantidade"]),
                preco_unitario=float(row["preco_unitario"]),
                faturamento=float(row["faturamento"]),
            )

            session.add(sale)
            existing_ids.add(sale_id)
            report["importados"] += 1

        session.commit()

    except Exception:
        session.rollback()
        raise

    return report
