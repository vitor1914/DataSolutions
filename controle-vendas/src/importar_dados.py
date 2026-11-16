
from pathlib import Path
from datetime import datetime

import pandas as pd


# ==========================================================
# CONFIGURAÇÕES DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_DADOS = BASE_DIR / "data" / "vendas_brutas.csv"
ARQUIVO_RELATORIO = BASE_DIR / "outputs" / "relatorio_diagnostico.txt"

COLUNAS_NUMERICAS = ["quantidade", "preco_unitario"]


# ==========================================================
# 1. IMPORTAÇÃO DOS DADOS
# ==========================================================

def importar_dados():
    """Importa a base bruta de vendas."""

    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    df = pd.read_csv(ARQUIVO_DADOS)

    return df


# ==========================================================
# 2. ANÁLISE DOS DADOS
# ==========================================================

def analisar_dados(df):
    """Realiza o diagnóstico inicial da base de vendas."""

    # Valores ausentes
    valores_ausentes = df.isnull().sum()

    # Registros duplicados
    registros_duplicados = int(df.duplicated().sum())

    # Valores negativos nas colunas numéricas
    colunas_numericas = df.select_dtypes(include="number")

    valores_negativos = colunas_numericas.lt(0).sum()

    # Tipos de dados
    tipos_dados = df.dtypes

    # Validação de campos numéricos
    valores_invalidos = {}

    for coluna in COLUNAS_NUMERICAS:
        if coluna in df.columns:
            convertidos = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

            invalidos = (
                df[coluna].notna() & convertidos.isna()
            ).sum()

            valores_invalidos[coluna] = int(invalidos)

    diagnostico = {
        "nome_arquivo": ARQUIVO_DADOS.name,
        "data_geracao": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        "total_registros": int(df.shape[0]),
        "total_colunas": int(df.shape[1]),
        "valores_ausentes": valores_ausentes,
        "total_ausentes": int(valores_ausentes.sum()),
        "registros_duplicados": registros_duplicados,
        "valores_negativos": valores_negativos,
        "total_negativos": int(valores_negativos.sum()),
        "tipos_dados": tipos_dados,
        "valores_invalidos": valores_invalidos,
        "total_invalidos": sum(valores_invalidos.values())
    }

    return diagnostico


# ==========================================================
# 3. IDENTIFICAÇÃO DOS PROBLEMAS
# ==========================================================

def identificar_problemas(diagnostico):
    """Organiza os problemas encontrados no diagnóstico."""

    problemas = []

    # Valores ausentes
    if diagnostico["total_ausentes"] > 0:
        for coluna, quantidade in diagnostico[
            "valores_ausentes"
        ].items():

            if quantidade > 0:
                problemas.append(
                    f"Valores ausentes na coluna '{coluna}': "
                    f"{quantidade}"
                )

    # Registros duplicados
    if diagnostico["registros_duplicados"] > 0:
        problemas.append(
            f"Registros duplicados: "
            f"{diagnostico['registros_duplicados']}"
        )

    # Valores negativos
    if diagnostico["total_negativos"] > 0:
        for coluna, quantidade in diagnostico[
            "valores_negativos"
        ].items():

            if quantidade > 0:
                problemas.append(
                    f"Valores negativos na coluna '{coluna}': "
                    f"{quantidade}"
                )

    # Valores numéricos inválidos
    if diagnostico["total_invalidos"] > 0:
        for coluna, quantidade in diagnostico[
            "valores_invalidos"
        ].items():

            if quantidade > 0:
                problemas.append(
                    f"Valores numéricos inválidos na coluna "
                    f"'{coluna}': {quantidade}"
                )

    return problemas


# ==========================================================
# 4. CONCLUSÃO TÉCNICA
# ==========================================================

def gerar_conclusao(diagnostico):
    """Gera uma conclusão baseada nos resultados encontrados."""

    problemas = []

    if diagnostico["total_ausentes"] > 0:
        problemas.append(
            f"{diagnostico['total_ausentes']} valor(es) ausente(s)"
        )

    if diagnostico["registros_duplicados"] > 0:
        problemas.append(
            f"{diagnostico['registros_duplicados']} registro(s) duplicado(s)"
        )

    if diagnostico["total_negativos"] > 0:
        problemas.append(
            f"{diagnostico['total_negativos']} valor(es) negativo(s)"
        )

    if diagnostico["total_invalidos"] > 0:
        problemas.append(
            f"{diagnostico['total_invalidos']} valor(es) numérico(s) inválido(s)"
        )

    if not problemas:
        return (
            "Não foram identificadas inconsistências nos critérios "
            "avaliados neste diagnóstico. A base pode seguir para "
            "as próximas etapas de validação e análise."
        )

    resumo = ", ".join(problemas)

    return (
        f"Foram identificados os seguintes pontos de atenção: {resumo}. "
        "Recomenda-se avaliar e tratar as inconsistências antes de "
        "utilizar a base em análises comerciais. "
        "Os dados originais não foram alterados."
    )


# ==========================================================
# 5. GERAÇÃO DO RELATÓRIO
# ==========================================================

def gerar_relatorio(diagnostico):
    """Gera e salva o relatório de diagnóstico em formato TXT."""

    problemas = identificar_problemas(diagnostico)

    linhas = []

    linhas.append("=" * 65)
    linhas.append("DATASOLUTIONS")
    linhas.append("RELATÓRIO DE DIAGNÓSTICO DE DADOS")
    linhas.append("=" * 65)

    # 1. Identificação da base
    linhas.append("\n1. IDENTIFICAÇÃO DA BASE")
    linhas.append("-" * 65)
    linhas.append(
        f"Arquivo analisado: {diagnostico['nome_arquivo']}"
    )
    linhas.append(
        f"Data da análise: {diagnostico['data_geracao']}"
    )

    # 2. Dimensões da base
    linhas.append("\n2. DIMENSÕES DA BASE")
    linhas.append("-" * 65)
    linhas.append(
        f"Total de registros: {diagnostico['total_registros']}"
    )
    linhas.append(
        f"Total de colunas: {diagnostico['total_colunas']}"
    )

    # 3. Valores ausentes
    linhas.append("\n3. VALORES AUSENTES")
    linhas.append("-" * 65)

    for coluna, quantidade in diagnostico[
        "valores_ausentes"
    ].items():

        linhas.append(f"{coluna}: {quantidade}")

    linhas.append(
        f"Total de valores ausentes: "
        f"{diagnostico['total_ausentes']}"
    )

    # 4. Registros duplicados
    linhas.append("\n4. REGISTROS DUPLICADOS")
    linhas.append("-" * 65)
    linhas.append(
        f"Total de registros duplicados: "
        f"{diagnostico['registros_duplicados']}"
    )

    # 5. Valores negativos
    linhas.append("\n5. VALORES NEGATIVOS")
    linhas.append("-" * 65)

    for coluna, quantidade in diagnostico[
        "valores_negativos"
    ].items():

        linhas.append(f"{coluna}: {quantidade}")

    linhas.append(
        f"Total de valores negativos: "
        f"{diagnostico['total_negativos']}"
    )

    # 6. Tipos de dados
    linhas.append("\n6. TIPOS DE DADOS")
    linhas.append("-" * 65)

    for coluna, tipo in diagnostico["tipos_dados"].items():
        linhas.append(f"{coluna}: {tipo}")

    # 7. Problemas identificados
    linhas.append("\n7. PROBLEMAS IDENTIFICADOS")
    linhas.append("-" * 65)

    if problemas:
        for indice, problema in enumerate(problemas, start=1):
            linhas.append(f"{indice}. {problema}")
    else:
        linhas.append("Nenhum problema identificado.")

    # 8. Conclusão técnica
    linhas.append("\n8. CONCLUSÃO TÉCNICA")
    linhas.append("-" * 65)
    linhas.append(gerar_conclusao(diagnostico))

    linhas.append("\n" + "=" * 65)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("=" * 65)

    conteudo = "\n".join(linhas)

    # Cria a pasta de saída caso ela não exista
    ARQUIVO_RELATORIO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ARQUIVO_RELATORIO.write_text(
        conteudo,
        encoding="utf-8"
    )

    return conteudo


# ==========================================================
# 6. EXECUÇÃO PRINCIPAL
# ==========================================================

def main():
    """Executa o processo completo de diagnóstico."""

    print("\nIniciando diagnóstico da base de vendas...")

    df = importar_dados()

    print("Base importada com sucesso!")

    diagnostico = analisar_dados(df)

    relatorio = gerar_relatorio(diagnostico)

    print("\n" + relatorio)

    print(
        f"\nRelatório salvo com sucesso em:\n"
        f"{ARQUIVO_RELATORIO}"
    )


if __name__ == "__main__":
    main()
