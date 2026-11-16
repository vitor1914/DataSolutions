
from pathlib import Path
from datetime import datetime

import pandas as pd


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_TRATADO = BASE_DIR / "data" / "vendas_tratadas.csv"

ARQUIVO_RELATORIO = (
    BASE_DIR / "outputs" / "relatorio_base_tratada.txt"
)


def importar_base_tratada():
    """Carrega a base tratada."""

    if not ARQUIVO_TRATADO.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_TRATADO}"
        )

    df = pd.read_csv(ARQUIVO_TRATADO)

    return df


def validar_base(df):
    """Executa as validações da base tratada."""

    resultados = {}

    # 1. Verificar estrutura
    colunas_obrigatorias = [
        "id_venda",
        "data_venda",
        "produto",
        "categoria",
        "quantidade",
        "preco_unitario",
        "vendedor",
        "regiao"
    ]

    colunas_ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    resultados["colunas_ausentes"] = colunas_ausentes

    if colunas_ausentes:
        return resultados

    # 2. Identificadores
    ids_ausentes = int(df["id_venda"].isna().sum())

    ids_repetidos = int(
        df["id_venda"].duplicated().sum()
    )

    resultados["ids_ausentes"] = ids_ausentes
    resultados["ids_repetidos"] = ids_repetidos

    # 3. Registros totalmente duplicados
    duplicados = int(df.duplicated().sum())

    resultados["linhas_duplicadas"] = duplicados

    # 4. Datas
    datas = pd.to_datetime(
        df["data_venda"],
        errors="coerce"
    )

    datas_ausentes = int(df["data_venda"].isna().sum())

    datas_invalidas = int(
        (df["data_venda"].notna() & datas.isna()).sum()
    )

    resultados["datas_ausentes"] = datas_ausentes
    resultados["datas_invalidas"] = datas_invalidas

    # 5. Quantidade
    quantidade = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    resultados["quantidade_ausente_ou_invalida"] = int(
        quantidade.isna().sum()
    )

    resultados["quantidade_menor_ou_igual_zero"] = int(
        (quantidade.notna() & (quantidade <= 0)).sum()
    )

    # 6. Preço unitário
    preco = pd.to_numeric(
        df["preco_unitario"],
        errors="coerce"
    )

    resultados["preco_ausente_ou_invalido"] = int(
        preco.isna().sum()
    )

    resultados["preco_menor_ou_igual_zero"] = int(
        (preco.notna() & (preco <= 0)).sum()
    )

    # 7. Campos obrigatórios
    campos = [
        "produto",
        "categoria",
        "vendedor",
        "regiao"
    ]

    resultados["campos_vazios"] = {}

    for coluna in campos:

        vazios = (
            df[coluna].isna()
            | df[coluna].astype("string").str.strip().eq("").fillna(False)
        )

        resultados["campos_vazios"][coluna] = int(
            vazios.sum()
        )

    return resultados


def verificar_aprovacao(resultados):
    """Determina se a base passou nas validações."""

    if resultados["colunas_ausentes"]:
        return False

    verificacoes = [
        resultados["ids_ausentes"],
        resultados["ids_repetidos"],
        resultados["linhas_duplicadas"],
        resultados["datas_ausentes"],
        resultados["datas_invalidas"],
        resultados["quantidade_ausente_ou_invalida"],
        resultados["quantidade_menor_ou_igual_zero"],
        resultados["preco_ausente_ou_invalido"],
        resultados["preco_menor_ou_igual_zero"]
    ]

    if any(valor > 0 for valor in verificacoes):
        return False

    if any(
        valor > 0
        for valor in resultados["campos_vazios"].values()
    ):
        return False

    return True


def gerar_relatorio(df, resultados, aprovado):
    """Gera o relatório final de validação."""

    linhas = []

    linhas.append("=" * 60)
    linhas.append("DATASOLUTIONS")
    linhas.append("RELATÓRIO DE VALIDAÇÃO DA BASE TRATADA")
    linhas.append("=" * 60)

    linhas.append("\n1. IDENTIFICAÇÃO")
    linhas.append("-" * 60)

    linhas.append("Arquivo: vendas_tratadas.csv")
    linhas.append(
        f"Data da validação: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    linhas.append("\n2. DIMENSÕES")
    linhas.append("-" * 60)

    linhas.append(f"Registros: {len(df)}")
    linhas.append(f"Colunas: {len(df.columns)}")

    linhas.append("\n3. RESULTADOS DAS VALIDAÇÕES")
    linhas.append("-" * 60)

    if resultados["colunas_ausentes"]:
        linhas.append(
            "Colunas obrigatórias ausentes: "
            + ", ".join(resultados["colunas_ausentes"])
        )
    else:
        linhas.append("Estrutura: OK")

        verificacoes = {
            "IDs ausentes": "ids_ausentes",
            "IDs repetidos": "ids_repetidos",
            "Linhas duplicadas": "linhas_duplicadas",
            "Datas ausentes": "datas_ausentes",
            "Datas inválidas": "datas_invalidas",
            "Quantidade ausente ou inválida":
                "quantidade_ausente_ou_invalida",
            "Quantidade menor ou igual a zero":
                "quantidade_menor_ou_igual_zero",
            "Preço ausente ou inválido":
                "preco_ausente_ou_invalido",
            "Preço menor ou igual a zero":
                "preco_menor_ou_igual_zero"
        }

        for descricao, chave in verificacoes.items():
            linhas.append(
                f"{descricao}: {resultados[chave]}"
            )

        linhas.append("\nCampos obrigatórios:")

        for coluna, quantidade in resultados["campos_vazios"].items():
            linhas.append(
                f"  {coluna}: {quantidade}"
            )

    linhas.append("\n4. CONCLUSÃO")
    linhas.append("-" * 60)

    if aprovado:
        linhas.append(
            "APROVADA: nenhum problema foi encontrado."
        )
        linhas.append(
            "A base passou nas verificações de qualidade."
        )
    else:
        linhas.append(
            "REPROVADA: foram encontradas inconsistências."
        )
        linhas.append(
            "A base precisa de nova análise antes de ser utilizada."
        )

    linhas.append("\n" + "=" * 60)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("=" * 60)

    conteudo = "\n".join(linhas)

    ARQUIVO_RELATORIO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ARQUIVO_RELATORIO.write_text(
        conteudo,
        encoding="utf-8"
    )

    return conteudo


def main():

    print("=" * 60)
    print("DATASOLUTIONS - VALIDAÇÃO DA BASE TRATADA")
    print("=" * 60)

    df = importar_base_tratada()

    resultados = validar_base(df)

    aprovado = verificar_aprovacao(resultados)

    relatorio = gerar_relatorio(
        df,
        resultados,
        aprovado
    )

    print("\n" + relatorio)

    print(
        f"\nRelatório salvo em: {ARQUIVO_RELATORIO}"
    )


if __name__ == "__main__":
    main()
