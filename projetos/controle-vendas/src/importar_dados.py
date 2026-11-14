
from pathlib import Path
import pandas as pd


# ==================================================
# CONFIGURAÇÕES DO PROJETO
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_DADOS = BASE_DIR / "data" / "vendas_brutas.csv"


# ==================================================
# IMPORTAÇÃO E DIAGNÓSTICO DOS DADOS
# ==================================================

def importar_dados():
    """Importa a base bruta de vendas e realiza diagnóstico inicial."""

    # Verificar existência do arquivo
    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    # Importar dados
    df = pd.read_csv(ARQUIVO_DADOS)

    print("\n" + "=" * 50)
    print("       DATASOLUTIONS - DIAGNÓSTICO DE DADOS")
    print("=" * 50)

    # 1. Confirmação da importação
    print("\n========== IMPORTAÇÃO ==========")
    print("Base importada com sucesso!")

    # 2. Primeiros registros
    print("\n========== PRIMEIROS REGISTROS ==========")
    print(df.head())

    # 3. Informações gerais
    print("\n========== INFORMAÇÕES DA BASE ==========")
    df.info()

    # 4. Dimensões
    print("\n========== DIMENSÕES ==========")
    print(f"Quantidade de registros: {df.shape[0]}")
    print(f"Quantidade de colunas: {df.shape[1]}")

    # 5. Valores ausentes
    print("\n========== VALORES AUSENTES ==========")
    ausentes = df.isnull().sum()

    print(ausentes)

    print(f"\nTotal de valores ausentes: {ausentes.sum()}")

    # 6. Registros duplicados
    print("\n========== REGISTROS DUPLICADOS ==========")
    duplicados = df.duplicated()

    print(f"Quantidade de registros duplicados: {duplicados.sum()}")

    if duplicados.any():
        print("\nRegistros duplicados encontrados:")
        print(df[duplicados])

    # 7. Valores negativos
    print("\n========== VALORES NEGATIVOS ==========")
    numericos = df.select_dtypes(include="number")

    negativos = numericos.lt(0).sum()

    print(negativos)

    print(f"\nTotal de valores negativos: {negativos.sum()}")

    # 8. Tipos de dados
    print("\n========== TIPOS DE DADOS ==========")
    print(df.dtypes)

    # 9. Estatísticas descritivas
    print("\n========== ESTATÍSTICAS DESCRITIVAS ==========")
    print(df.describe())

    # 10. Valores inválidos nas colunas numéricas
    print("\n========== VALIDAÇÃO NUMÉRICA ==========")

    for coluna in ["quantidade", "preco_unitario"]:
        if coluna in df.columns:
            valores = pd.to_numeric(df[coluna], errors="coerce")

            invalidos = valores.isnull().sum()
            print(f"{coluna}: {invalidos} valor(es) ausente(s) ou inválido(s)")

    # 11. Resumo do diagnóstico
    print("\n========== RESUMO DO DIAGNÓSTICO ==========")
    print(f"Registros analisados: {len(df)}")
    print(f"Colunas analisadas: {len(df.columns)}")
    print(f"Valores ausentes: {ausentes.sum()}")
    print(f"Registros duplicados: {duplicados.sum()}")
    print(f"Valores negativos: {negativos.sum()}")

    print("\n========== DIAGNÓSTICO FINALIZADO ==========")

    return df


# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================

if __name__ == "__main__":
    dados = importar_dados()
