
from pathlib import Path

from importar_dados import importar_dados
from validar_dados import validar_dados
from gerar_relatorio import gerar_relatorio as gerar_relatorio_original

from tratar_dados import tratar_dados

from validar_base_tratada import (
    importar_base_tratada,
    validar_base,
    verificar_aprovacao,
    gerar_relatorio as gerar_relatorio_tratado
)


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_RELATORIO_ORIGINAL = (
    BASE_DIR / "outputs" / "relatorio_validacao.txt"
)

ARQUIVO_RELATORIO_TRATADO = (
    BASE_DIR / "outputs" / "relatorio_base_tratada.txt"
)


def executar_pipeline():
    """Executa todas as etapas do projeto DataSolutions."""

    print("=" * 60)
    print("DATASOLUTIONS - PIPELINE DE DADOS")
    print("=" * 60)

    # ETAPA 1 - Importação
    print("\n[1/5] IMPORTAÇÃO DOS DADOS")
    print("-" * 60)

    df_original = importar_dados()

    print(f"Registros importados: {len(df_original)}")

    # ETAPA 2 - Validação da base original
    print("\n[2/5] VALIDAÇÃO DA BASE ORIGINAL")
    print("-" * 60)

    resultados_originais = validar_dados(df_original)

    gerar_relatorio_original(
        df_original,
        resultados_originais
    )

    print("Validação original concluída.")
    print(f"Relatório: {ARQUIVO_RELATORIO_ORIGINAL}")

    # ETAPA 3 - Tratamento dos dados
    print("\n[3/5] TRATAMENTO DOS DADOS")
    print("-" * 60)

    validos, pendentes = tratar_dados(df_original)

    print(f"Registros originais: {len(df_original)}")
    print(f"Registros válidos: {len(validos)}")
    print(f"Registros pendentes: {len(pendentes)}")

    print("\nArquivos gerados:")
    print("data/vendas_tratadas.csv")
    print("outputs/registros_pendentes.csv")

    # ETAPA 4 - Validação da base tratada
    print("\n[4/5] VALIDAÇÃO DA BASE TRATADA")
    print("-" * 60)

    df_tratado = importar_base_tratada()

    resultados_tratados = validar_base(df_tratado)

    aprovado = verificar_aprovacao(resultados_tratados)

    print(f"Registros avaliados: {len(df_tratado)}")

    # ETAPA 5 - Relatório e conclusão
    print("\n[5/5] GERAÇÃO DO RELATÓRIO FINAL")
    print("-" * 60)

    relatorio = gerar_relatorio_tratado(
        df_tratado,
        resultados_tratados,
        aprovado
    )

    print(relatorio)

    print(f"\nRelatório salvo em: {ARQUIVO_RELATORIO_TRATADO}")

    print("\n" + "=" * 60)
    print("RESULTADO DO PIPELINE")
    print("=" * 60)

    if aprovado:
        print("STATUS: BASE TRATADA APROVADA")
    else:
        print("STATUS: BASE TRATADA REPROVADA")

    print(f"Registros processados: {len(df_original)}")
    print(f"Registros aproveitados: {len(df_tratado)}")
    print(f"Registros pendentes: {len(pendentes)}")

    print("\nPipeline executado até o final.")
    print("A base original foi preservada.")

    print("=" * 60)


if __name__ == "__main__":
    executar_pipeline()
