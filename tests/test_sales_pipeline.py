
import pandas as pd
import pytest

from src.datapulse.pipeline.sales_pipeline import (
    clean_sales_data,
    load_sales_csv,
)


def test_clean_sales_data_removes_invalid_and_duplicate_rows():
    raw = pd.DataFrame(
        [
            ["V001", "2026-10-01", "Teclado", 2, 120.00],
            ["V001", "2026-10-01", "Teclado", 2, 120.00],
            ["V002", "2026-10-02", "Mouse", 3, 45.50],
            ["V003", "data-invalida", "Monitor", 1, 899.90],
            ["V004", "2026-10-03", "Cabo", 0, 20.00],
        ],
        columns=[
            "id_venda",
            "data",
            "produto",
            "quantidade",
            "preco_unitario",
        ],
    )

    clean, report = clean_sales_data(raw)

    assert len(clean) == 2
    assert clean["id_venda"].tolist() == ["V001", "V002"]
    assert report["duplicados"] == 1
    assert report["com_campos_ausentes_ou_invalidos"] == 1
    assert report["com_valores_fora_das_regras"] == 1
    assert report["rejeitados"] == 3


def test_faturamento_is_calculated_correctly():
    raw = pd.DataFrame(
        [
            ["V001", "2026-10-01", "Teclado", 2, 120.00],
        ],
        columns=[
            "id_venda",
            "data",
            "produto",
            "quantidade",
            "preco_unitario",
        ],
    )

    clean, _ = clean_sales_data(raw)

    assert clean.iloc[0]["faturamento"] == 240.00


def test_load_sales_csv_requires_all_columns(tmp_path):
    csv_file = tmp_path / "incompleto.csv"
    csv_file.write_text(
        "id_venda,data,produto\nV001,2026-10-01,Teclado\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        load_sales_csv(csv_file)

