import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import executar_pipeline as modulo_pipeline
import tratar_dados as modulo_tratamento
import gerar_relatorio as modulo_relatorio
import validar_base_tratada as modulo_validacao_tratada


def test_pipeline_execucao_com_sucesso(tmp_path, monkeypatch):
    """Deve executar as cinco etapas e registrar sucesso."""

    # Base de teste com dois registros válidos
    df = pd.DataFrame({
        "id_venda": [101, 102],
        "data_venda": ["2026-11-01", "2026-11-02"],
        "produto": ["Notebook", "Mouse"],
        "categoria": ["Eletronicos", "Perifericos"],
        "quantidade": [2, 5],
        "preco_unitario": [3500.0, 80.0],
        "vendedor": ["Joao", "Maria"],
        "regiao": ["Sudeste", "Sul"]
    })

    # Diretório temporário para todos os arquivos
    pasta = tmp_path / "outputs"
    dados = tmp_path / "data"

    arquivo_tratado = dados / "vendas_tratadas.csv"
    arquivo_pendente = pasta / "registros_pendentes.csv"

    # Isola os arquivos do tratamento
    monkeypatch.setattr(
        modulo_tratamento,
        "ARQUIVO_TRATADO",
        arquivo_tratado
    )

    monkeypatch.setattr(
        modulo_tratamento,
        "ARQUIVO_PENDENTE",
        arquivo_pendente
    )

    # Isola a importação da base tratada
    monkeypatch.setattr(
        modulo_validacao_tratada,
        "ARQUIVO_TRATADO",
        arquivo_tratado
    )

    # Isola os relatórios
    monkeypatch.setattr(
        modulo_pipeline,
        "ARQUIVO_RELATORIO_ORIGINAL",
        pasta / "relatorio_validacao.txt"
    )

    monkeypatch.setattr(
        modulo_pipeline,
        "ARQUIVO_RELATORIO_AUDITORIA",
        pasta / "relatorio_auditoria.txt"
    )

    monkeypatch.setattr(
        modulo_pipeline,
        "ARQUIVO_RELATORIO_TRATADO",
        pasta / "relatorio_base_tratada.txt"
    )

    monkeypatch.setattr(
        modulo_relatorio,
        "ARQUIVO_RELATORIO",
        pasta / "relatorio_validacao.txt"
    )

    monkeypatch.setattr(
        modulo_validacao_tratada,
        "ARQUIVO_RELATORIO",
        pasta / "relatorio_base_tratada.txt"
    )

    # Fornece a base de teste ao pipeline
    monkeypatch.setattr(
        modulo_pipeline,
        "importar_dados",
        lambda: df.copy()
    )

    # Captura o registro do histórico sem alterar o histórico real
    registros_log = []

    monkeypatch.setattr(
        modulo_pipeline,
        "registrar_log",
        lambda *args: registros_log.append(args)
    )

    # Executa o pipeline completo
    modulo_pipeline.executar_pipeline()

    # Verifica os arquivos gerados
    assert arquivo_tratado.exists()
    assert arquivo_pendente.exists()

    assert (pasta / "relatorio_validacao.txt").exists()
    assert (pasta / "relatorio_auditoria.txt").exists()
    assert (pasta / "relatorio_base_tratada.txt").exists()

    # Verifica os registros tratados
    resultado = pd.read_csv(arquivo_tratado)

    assert len(resultado) == 2
    assert resultado["id_venda"].tolist() == [101, 102]

    # Verifica que não houve pendências
    pendentes = pd.read_csv(arquivo_pendente)

    assert len(pendentes) == 0

    # Verifica o registro de sucesso
    assert len(registros_log) == 1
    assert registros_log[0][4] == "APROVADA"
    assert registros_log[0][5] == "SUCESSO"
    assert registros_log[0][6] == ""
