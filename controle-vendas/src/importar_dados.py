
from pathlib import Path
import pandas as pd


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = BASE_DIR / "data" / "vendas_brutas.csv"


def importar_dados():
    """Importa a base bruta de vendas."""

    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    df = pd.read_csv(ARQUIVO_DADOS)

    # Identifica cabeçalhos repetidos dentro dos registros
    cabecalho_repetido = (
        df["id_venda"].astype(str).str.strip() == "id_venda"
    )

    quantidade_cabecalhos = int(cabecalho_repetido.sum())

    if quantidade_cabecalhos > 0:
        print(
            f"Cabeçalhos repetidos encontrados: "
            f"{quantidade_cabecalhos}"
        )

        df = df.loc[~cabecalho_repetido].copy()

    print("Base importada com sucesso!")
    print(f"Registros carregados: {len(df)}")
    print(f"Colunas identificadas: {len(df.columns)}")

    return df


if __name__ == "__main__":
    dados = importar_dados()
    print("\nPrimeiros registros:")
    print(dados.head())
