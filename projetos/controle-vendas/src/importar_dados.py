
from pathlib import Path
import pandas as pd

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho da base de dados
ARQUIVO_DADOS = BASE_DIR / "data" / "vendas_brutas.csv"

def importar_dados():
    """Importa a base bruta de vendas utilizando Pandas."""

    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    df = pd.read_csv(ARQUIVO_DADOS)

    print("\n========== IMPORTAÇÃO DE DADOS ==========")
    print("Base importada com sucesso!")

    print("\n========== PRIMEIROS REGISTROS ==========")
    print(df.head())

    print("\n========== INFORMAÇÕES DA BASE ==========")
    df.info()

    print("\n========== DIMENSÕES ==========")
    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}")

    print("\n========== VALORES AUSENTES ==========")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":
    dados = importar_dados()
