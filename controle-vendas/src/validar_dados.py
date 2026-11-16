
import pandas as pd

from importar_dados import importar_dados


def validar_identificadores(df):
    """Valida os identificadores das vendas."""

    ids_ausentes = df["id_venda"].isna().sum()

    ids_repetidos = df[
        df.duplicated(subset=["id_venda"], keep=False)
    ].copy()

    linhas_duplicadas = df[
        df.duplicated(keep=False)
    ].copy()

    total_linhas_duplicadas = int(df.duplicated().sum())

    return {
        "ids_ausentes": int(ids_ausentes),
        "ids_repetidos": ids_repetidos,
        "linhas_duplicadas": linhas_duplicadas,
        "total_linhas_duplicadas": total_linhas_duplicadas
    }


def validar_datas(df):
    """Valida e converte as datas das vendas."""

    datas_convertidas = pd.to_datetime(
        df["data_venda"],
        errors="coerce"
    )

    datas_ausentes = int(df["data_venda"].isna().sum())

    datas_invalidas = int(
        (df["data_venda"].notna() & datas_convertidas.isna()).sum()
    )

    return {
        "datas_convertidas": datas_convertidas,
        "datas_ausentes": datas_ausentes,
        "datas_invalidas": datas_invalidas
    }


def validar_regras_comerciais(df):
    """Valida as regras comerciais da base."""

    resultados = {}

    # Quantidade deve ser maior que zero
    quantidade = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    resultados["quantidade"] = {
        "ausentes": int(quantidade.isna().sum()),
        "invalidos": int(
            (quantidade.notna() & (quantidade <= 0)).sum()
        )
    }

    # Preço unitário deve ser maior que zero
    preco = pd.to_numeric(
        df["preco_unitario"],
        errors="coerce"
    )

    resultados["preco_unitario"] = {
        "ausentes": int(preco.isna().sum()),
        "invalidos": int(
            (preco.notna() & (preco <= 0)).sum()
        )
    }

    # Campos obrigatórios não podem estar vazios
    for coluna in ["produto", "categoria", "vendedor", "regiao"]:

        vazios = (
            df[coluna].isna()
            | df[coluna].astype("string").str.strip().eq("").fillna(False)
        )

        resultados[coluna] = {
            "ausentes": int(vazios.sum())
        }

    return resultados


def validar_dados(df):
    """Executa todas as validações da base."""

    identificadores = validar_identificadores(df)

    datas = validar_datas(df)

    comercial = validar_regras_comerciais(df)

    return {
        "identificadores": identificadores,
        "datas": datas,
        "comercial": comercial
    }


def exibir_resultados(resultados):
    """Exibe os resultados da validação."""

    print("\n" + "=" * 55)
    print("DATASOLUTIONS - VALIDAÇÃO DE DADOS")
    print("=" * 55)

    # Identificadores
    identificadores = resultados["identificadores"]

    print("\n1. VALIDAÇÃO DOS IDENTIFICADORES")
    print("-" * 55)

    print(f"IDs ausentes: {identificadores['ids_ausentes']}")
    print(
        "Linhas totalmente duplicadas: "
        f"{identificadores['total_linhas_duplicadas']}"
    )

    print(
        "Quantidade de linhas envolvidas em IDs repetidos: "
        f"{len(identificadores['ids_repetidos'])}"
    )

    if not identificadores["ids_repetidos"].empty:
        print("\nRegistros com IDs repetidos:")
        print(identificadores["ids_repetidos"].to_string(index=False))

    # Datas
    datas = resultados["datas"]

    print("\n2. VALIDAÇÃO DAS DATAS")
    print("-" * 55)

    print(f"Datas ausentes: {datas['datas_ausentes']}")
    print(f"Datas inválidas: {datas['datas_invalidas']}")

    # Regras comerciais
    comercial = resultados["comercial"]

    print("\n3. VALIDAÇÃO COMERCIAL")
    print("-" * 55)

    for coluna, dados in comercial.items():
        print(f"\n{coluna}:")

        for tipo, quantidade in dados.items():
            print(f"  {tipo.capitalize()}: {quantidade}")

    print("\n" + "=" * 55)
    print("VALIDAÇÃO FINALIZADA")
    print("=" * 55)


def main():
    df = importar_dados()

    resultados = validar_dados(df)

    exibir_resultados(resultados)


if __name__ == "__main__":
    main()
