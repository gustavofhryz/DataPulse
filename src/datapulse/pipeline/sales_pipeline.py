
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "id_venda",
    "data",
    "produto",
    "quantidade",
    "preco_unitario",
]


def load_sales_csv(file_path: str | Path) -> pd.DataFrame:
    """Carrega um CSV de vendas e verifica suas colunas obrigatórias."""
    df = pd.read_csv(file_path, dtype={"id_venda": "string"})

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing_columns}"
        )

    return df[REQUIRED_COLUMNS].copy()


def clean_sales_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Limpa e valida vendas, retornando os dados e um relatório."""
    result = df.copy()
    report = {"recebidos": len(result)}

    # Normalizar textos e remover espaços desnecessários.
    for column in ["id_venda", "produto"]:
        result[column] = result[column].astype("string").str.strip()

    # Converter os campos para os tipos corretos.
    result["data"] = pd.to_datetime(
        result["data"], errors="coerce"
    )
    result["quantidade"] = pd.to_numeric(
        result["quantidade"], errors="coerce"
    )
    result["preco_unitario"] = pd.to_numeric(
        result["preco_unitario"], errors="coerce"
    )

    # Identificar registros sem campos obrigatórios.
    missing = result[REQUIRED_COLUMNS].isna().any(axis=1)
    report["com_campos_ausentes_ou_invalidos"] = int(missing.sum())
    result = result.loc[~missing].copy()

    # Quantidade deve ser inteira e positiva.
    valid_quantity = (
        result["quantidade"].gt(0)
        & result["quantidade"].mod(1).eq(0)
    )

    # O preço precisa ser positivo.
    valid_price = result["preco_unitario"].gt(0)

    invalid = ~(valid_quantity & valid_price)
    report["com_valores_fora_das_regras"] = int(invalid.sum())
    result = result.loc[~invalid].copy()

    # Cada identificador de venda deve aparecer apenas uma vez.
    duplicate = result.duplicated(subset=["id_venda"], keep="first")
    report["duplicados"] = int(duplicate.sum())
    result = result.loc[~duplicate].copy()

    # Definir tipos e criar a métrica de faturamento.
    result["quantidade"] = result["quantidade"].astype("int64")
    result["preco_unitario"] = result["preco_unitario"].astype("float64")
    result["faturamento"] = (
        result["quantidade"] * result["preco_unitario"]
    ).round(2)

    result = result.sort_values("data").reset_index(drop=True)
    report["aprovados"] = len(result)
    report["rejeitados"] = report["recebidos"] - report["aprovados"]

    return result, report


def process_sales_file(
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, int]:
    """Executa o pipeline completo e salva os dados limpos."""
    raw_data = load_sales_csv(input_path)
    clean_data, report = clean_sales_data(raw_data)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    clean_data.to_csv(
        destination,
        index=False,
        date_format="%Y-%m-%d",
    )

    return report
