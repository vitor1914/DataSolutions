
from pathlib import Path
from datetime import datetime

import pandas as pd

from importar_dados import importar_dados
from validar_dados import validar_dados


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_RELATORIO = BASE_DIR / "outputs" / "relatorio_validacao.txt"


def ids_dos_registros(df, mascara):
    """Retorna os IDs dos registros identificados por uma condição."""

    registros = df.loc[mascara]

    if registros.empty:
        return "Nenhum"

    if "id_venda" not in registros.columns:
        return "Não disponível"

    ids = registros["id_venda"].dropna().drop_duplicates().tolist()

    if registros["id_venda"].isna().any():
        ids.append("ID ausente")

    if not ids:
        return "ID ausente"

    return ", ".join(str(valor) for valor in ids)


def campo_ausente(df, coluna):
    """Identifica valores ausentes ou textos vazios."""

    return (
        df[coluna].isna()
        | df[coluna].astype(str).str.strip().eq("")
    )


def gerar_relatorio(df, resultados):
    """Gera o relatório de validação da base de vendas."""

    identificadores = resultados["identificadores"]
    datas = resultados["datas"]
    comercial = resultados["comercial"]

    linhas = []

    # Identificação dinâmica dos problemas
    ids_duplicados = df["id_venda"].duplicated(keep=False)

    registros_duplicados = df.duplicated(keep=False)

    quantidades = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    precos = pd.to_numeric(
        df["preco_unitario"],
        errors="coerce"
    )

    quantidade_invalida = quantidades.isna() | (quantidades <= 0)
    preco_ausente = precos.isna()

    produto_ausente = campo_ausente(df, "produto")
    regiao_ausente = campo_ausente(df, "regiao")

    linhas.append("=" * 65)
    linhas.append("DATASOLUTIONS")
    linhas.append("RELATÓRIO DE VALIDAÇÃO DE DADOS")
    linhas.append("=" * 65)

    # 1. Identificação
    linhas.append("\n1. IDENTIFICAÇÃO DA BASE")
    linhas.append("-" * 65)
    linhas.append("Arquivo analisado: vendas_brutas.csv")
    linhas.append(
        f"Data da validação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    # 2. Dimensões
    linhas.append("\n2. DIMENSÕES DA BASE")
    linhas.append("-" * 65)
    linhas.append(f"Registros analisados: {len(df)}")
    linhas.append(f"Colunas identificadas: {len(df.columns)}")

    # 3. Identificadores
    linhas.append("\n3. VALIDAÇÃO DOS IDENTIFICADORES")
    linhas.append("-" * 65)
    linhas.append(f"IDs ausentes: {identificadores['ids_ausentes']}")
    linhas.append(
        f"Linhas totalmente duplicadas: "
        f"{identificadores['total_linhas_duplicadas']}"
    )
    linhas.append(
        f"Linhas envolvidas em IDs repetidos: "
        f"{len(identificadores['ids_repetidos'])}"
    )

    linhas.append(
        f"IDs repetidos identificados: "
        f"{ids_dos_registros(df, ids_duplicados)}"
    )

    linhas.append(
        f"IDs em registros totalmente duplicados: "
        f"{ids_dos_registros(df, registros_duplicados)}"
    )

    if not identificadores["ids_repetidos"].empty:
        linhas.append("\nRegistros com IDs repetidos:")
        linhas.append(
            identificadores["ids_repetidos"].to_string(index=False)
        )

    if not identificadores["linhas_duplicadas"].empty:
        linhas.append("\nRegistros totalmente duplicados:")
        linhas.append(
            identificadores["linhas_duplicadas"].to_string(index=False)
        )

    # 4. Datas
    linhas.append("\n4. VALIDAÇÃO DAS DATAS")
    linhas.append("-" * 65)
    linhas.append(f"Datas ausentes: {datas['datas_ausentes']}")
    linhas.append(f"Datas inválidas: {datas['datas_invalidas']}")

    # 5. Regras comerciais
    linhas.append("\n5. VALIDAÇÃO COMERCIAL")
    linhas.append("-" * 65)

    for coluna, dados in comercial.items():
        linhas.append(f"\n{coluna}:")

        for tipo, quantidade in dados.items():
            linhas.append(f"  {tipo.capitalize()}: {quantidade}")

    # 6. Problemas identificados
    linhas.append("\n6. PROBLEMAS IDENTIFICADOS")
    linhas.append("-" * 65)

    problemas = []

    if identificadores["ids_repetidos"].shape[0] > 0:
        problemas.append(
            f"IDs de venda repetidos: "
            f"{ids_dos_registros(df, ids_duplicados)}."
        )

    if identificadores["total_linhas_duplicadas"] > 0:
        problemas.append(
            f"Registros totalmente duplicados: "
            f"{ids_dos_registros(df, registros_duplicados)}."
        )

    if datas["datas_ausentes"] > 0:
        problemas.append("Existem datas ausentes.")

    if datas["datas_invalidas"] > 0:
        problemas.append("Existem datas inválidas.")

    if comercial["quantidade"]["invalidos"] > 0:
        problemas.append(
            f"Quantidade inválida ou menor ou igual a zero: "
            f"investigar IDs {ids_dos_registros(df, quantidade_invalida)}."
        )

    if comercial["produto"]["ausentes"] > 0:
        problemas.append(
            f"Produto ausente: investigar IDs "
            f"{ids_dos_registros(df, produto_ausente)}."
        )

    if comercial["preco_unitario"]["ausentes"] > 0:
        problemas.append(
            f"Preço unitário ausente: investigar IDs "
            f"{ids_dos_registros(df, preco_ausente)}."
        )

    if comercial["regiao"]["ausentes"] > 0:
        problemas.append(
            f"Região ausente: investigar IDs "
            f"{ids_dos_registros(df, regiao_ausente)}."
        )

    if problemas:
        for indice, problema in enumerate(problemas, start=1):
            linhas.append(f"{indice}. {problema}")
    else:
        linhas.append("Nenhum problema identificado.")

    # 7. Proposta de tratamento
    linhas.append("\n7. PROPOSTA DE TRATAMENTO")
    linhas.append("-" * 65)

    propostas = []

    if identificadores["ids_repetidos"].shape[0] > 0:
        propostas.append(
            "Analisar os IDs repetidos e preservar as ocorrências "
            "até a aprovação manual."
        )

    if identificadores["total_linhas_duplicadas"] > 0:
        propostas.append(
            "Investigar os registros totalmente duplicados antes "
            "de qualquer exclusão."
        )

    if comercial["quantidade"]["invalidos"] > 0:
        propostas.append(
            "Investigar a origem das quantidades inválidas e "
            "confirmar os valores em fonte confiável."
        )

    if comercial["produto"]["ausentes"] > 0:
        propostas.append(
            "Buscar os produtos ausentes em uma fonte confiável."
        )

    if comercial["preco_unitario"]["ausentes"] > 0:
        propostas.append(
            "Verificar os preços ausentes em fonte confiável, "
            "sem inventar valores."
        )

    if comercial["regiao"]["ausentes"] > 0:
        propostas.append(
            "Verificar a possibilidade de recuperar as regiões ausentes."
        )

    if datas["datas_ausentes"] > 0 or datas["datas_invalidas"] > 0:
        propostas.append(
            "Investigar as datas ausentes ou inválidas e confirmar "
            "os valores de origem."
        )

    if propostas:
        for indice, proposta in enumerate(propostas, start=1):
            linhas.append(f"{indice}. {proposta}")
    else:
        linhas.append("Nenhuma ação corretiva necessária.")

    # 8. Conclusão
    linhas.append("\n8. CONCLUSÃO TÉCNICA")
    linhas.append("-" * 65)

    if problemas:
        linhas.append(
            "A base apresenta inconsistências que precisam ser avaliadas "
            "antes de sua utilização em análises comerciais."
        )
    else:
        linhas.append(
            "A base não apresentou inconsistências nas regras avaliadas."
        )

    linhas.append(
        "Nenhum registro foi excluído ou modificado nesta etapa."
    )

    linhas.append(
        "A geração da base tratada deverá respeitar as regras "
        "de validação e tratamento definidas no projeto."
    )

    linhas.append("\n" + "=" * 65)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("=" * 65)

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
    df = importar_dados()

    resultados = validar_dados(df)

    relatorio = gerar_relatorio(df, resultados)

    print("\n" + relatorio)

    print(
        f"\nRelatório salvo em: {ARQUIVO_RELATORIO}"
    )


if __name__ == "__main__":
    main()
