
from pathlib import Path

from importar_dados import importar_dados
from validar_dados import validar_dados
from auditoria_dados import auditar_dados, gerar_relatorio_auditoria
from gerar_relatorio import gerar_relatorio as gerar_relatorio_original

from tratar_dados import tratar_dados

from validar_base_tratada import (
    importar_base_tratada,
    validar_base,
    verificar_aprovacao,
    gerar_relatorio as gerar_relatorio_tratado
)

from registrar_log import registrar_log


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_RELATORIO_ORIGINAL = (
    BASE_DIR / "outputs" / "relatorio_validacao.txt"
)

ARQUIVO_RELATORIO_AUDITORIA = (
    BASE_DIR / "outputs" / "relatorio_auditoria.txt"
)

ARQUIVO_RELATORIO_TRATADO = (
    BASE_DIR / "outputs" / "relatorio_base_tratada.txt"
)


def executar_pipeline():
    """Executa todas as etapas e registra o histórico."""

    # Inicialização dos contadores
    registros_importados = 0
    registros_validos = 0
    registros_pendentes = 0
    registros_aprovados = 0

    status_validacao = "REPROVADA"

    print("=" * 60)
    print("DATASOLUTIONS - PIPELINE DE DADOS")
    print("=" * 60)

    try:

        # ETAPA 1 - Importação
        print("\n[1/5] IMPORTAÇÃO DOS DADOS")
        print("-" * 60)

        df_original = importar_dados()

        registros_importados = len(df_original)

        print(f"Registros importados: {registros_importados}")

        # ETAPA 2 - Validação da base original
        print("\n[2/5] VALIDAÇÃO DA BASE ORIGINAL")
        print("-" * 60)

        resultados_originais = validar_dados(df_original)

        # AUDITORIA DOS DADOS ORIGINAIS
        print("\nAUDITORIA DOS DADOS ORIGINAIS")
        print("-" * 60)

        auditoria = auditar_dados(
            df_original,
            resultados_originais
        )

        gerar_relatorio_auditoria(
            auditoria,
            ARQUIVO_RELATORIO_AUDITORIA
        )

        print("Auditoria concluída.")

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

        registros_validos = len(validos)
        registros_pendentes = len(pendentes)

        print(f"Registros originais: {registros_importados}")
        print(f"Registros válidos: {registros_validos}")
        print(f"Registros pendentes: {registros_pendentes}")

        print("\nArquivos gerados:")
        print("data/vendas_tratadas.csv")
        print("outputs/registros_pendentes.csv")

        # ETAPA 4 - Validação da base tratada
        print("\n[4/5] VALIDAÇÃO DA BASE TRATADA")
        print("-" * 60)

        df_tratado = importar_base_tratada()

        resultados_tratados = validar_base(df_tratado)

        aprovado = verificar_aprovacao(resultados_tratados)

        registros_aprovados = (
            len(df_tratado) if aprovado else 0
        )

        status_validacao = (
            "APROVADA" if aprovado else "REPROVADA"
        )

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

        print(f"Registros processados: {registros_importados}")
        print(f"Registros aproveitados: {len(df_tratado)}")
        print(f"Registros pendentes: {registros_pendentes}")

        print("\nPipeline executado até o final.")
        print("A base original foi preservada.")

        print("=" * 60)

        # Registrar execução concluída
        registrar_log(
            registros_importados,
            registros_validos,
            registros_pendentes,
            registros_aprovados,
            status_validacao,
            "SUCESSO",
            ""
        )

    except Exception as erro:

        # Registrar falha de execução
        registrar_log(
            registros_importados,
            registros_validos,
            registros_pendentes,
            registros_aprovados,
            status_validacao,
            "ERRO",
            str(erro)
        )

        print("\n" + "=" * 60)
        print("ERRO NA EXECUÇÃO DO PIPELINE")
        print("=" * 60)

        print(f"Mensagem: {erro}")

        print("=" * 60)

        raise


if __name__ == "__main__":
    executar_pipeline()
