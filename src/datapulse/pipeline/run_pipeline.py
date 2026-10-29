
from pathlib import Path

from src.datapulse.pipeline.sales_pipeline import process_sales_file


ROOT_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = ROOT_DIR / "data" / "raw" / "vendas.csv"
OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "vendas_limpas.csv"


def main() -> None:
    report = process_sales_file(INPUT_FILE, OUTPUT_FILE)

    print("\n=== DataPulse | Relatório do Pipeline ===")

    for name, value in report.items():
        print(f"{name.replace('_', ' ').capitalize()}: {value}")

    print(f"\nArquivo gerado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
