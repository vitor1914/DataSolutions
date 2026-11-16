
from pathlib import Path
from datetime import datetime

from importar_dados import importar_dados
from validar_dados import validar_dados


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_RELATORIO = BASE_DIR / "outputs" / "relatorio_validacao.txt"


def gerar_relatorio(df, resultados):
    """Gera o relatório de validação da base de vendas."""

    identificadores = resultados["identificadores"]
    datas = resultados["datas"]
    comercial = resultados["comercial"]

    linhas = []

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
            "Identificador de venda repetido: ID 9."
        )

    if identificadores["total_linhas_duplicadas"] > 0:
        problemas.append(
            "Registro totalmente duplicado: ID 9."
        )

    if datas["datas_ausentes"] > 0:
        problemas.append("Existem datas ausentes.")

    if datas["datas_invalidas"] > 0:
        problemas.append("Existem datas inválidas.")

    if comercial["quantidade"]["invalidos"] > 0:
        problemas.append(
            "Quantidade menor ou igual a zero: investigar ID 6."
        )

    if comercial["produto"]["ausentes"] > 0:
        problemas.append("Produto ausente: investigar ID 8.")

    if comercial["preco_unitario"]["ausentes"] > 0:
        problemas.append("Preço unitário ausente: investigar ID 10.")

    if comercial["regiao"]["ausentes"] > 0:
        problemas.append("Região ausente: investigar ID 12.")

    if problemas:
        for indice, problema in enumerate(problemas, start=1):
            linhas.append(f"{indice}. {problema}")
    else:
        linhas.append("Nenhum problema identificado.")

    # 7. Proposta de tratamento
    linhas.append("\n7. PROPOSTA DE TRATAMENTO")
    linhas.append("-" * 65)
    linhas.append(
        "ID 9: preservar as ocorrências até análise e aprovação manual."
    )
    linhas.append(
        "ID 6: investigar a origem da quantidade negativa."
    )
    linhas.append(
        "ID 8: buscar o produto em fonte confiável."
    )
    linhas.append(
        "ID 10: buscar o preço em fonte confiável, sem inventar valores."
    )
    linhas.append(
        "ID 12: verificar a possibilidade de recuperar a região."
    )

    # 8. Conclusão
    linhas.append("\n8. CONCLUSÃO TÉCNICA")
    linhas.append("-" * 65)
    linhas.append(
        "A base apresenta inconsistências que precisam ser avaliadas "
        "antes de sua utilização em análises comerciais."
    )
    linhas.append(
        "Nenhum registro foi excluído ou modificado nesta etapa."
    )
    linhas.append(
        "A geração da base tratada deverá ocorrer somente após "
        "a aprovação das regras de tratamento."
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
