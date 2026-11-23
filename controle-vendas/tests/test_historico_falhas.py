import sys
import csv
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import registrar_log as modulo_log


def test_registrar_erro_no_historico(tmp_path, monkeypatch):
    """Deve registrar a falha no histórico CSV."""

    pasta = tmp_path / "outputs"
    arquivo = pasta / "historico_execucoes.csv"

    monkeypatch.setattr(
        modulo_log,
        "PASTA_OUTPUTS",
        pasta
    )

    monkeypatch.setattr(
        modulo_log,
        "ARQUIVO_HISTORICO",
        arquivo
    )

    modulo_log.registrar_log(
        registros_importados=0,
        registros_validos=0,
        registros_pendentes=0,
        registros_aprovados=0,
        status_validacao="REPROVADA",
        status_execucao="ERRO",
        mensagem_erro="Falha simulada na importação"
    )

    assert arquivo.exists()

    with open(arquivo, newline="", encoding="utf-8") as arquivo_csv:
        registros = list(csv.DictReader(arquivo_csv))

    assert len(registros) == 1
    assert registros[0]["status_execucao"] == "ERRO"
    assert registros[0]["status_validacao"] == "REPROVADA"
    assert registros[0]["mensagem_erro"] == "Falha simulada na importação"


def test_historico_preserva_registros_anteriores(tmp_path, monkeypatch):
    """Deve acrescentar novos registros sem apagar os anteriores."""

    pasta = tmp_path / "outputs"
    arquivo = pasta / "historico_execucoes.csv"

    monkeypatch.setattr(modulo_log, "PASTA_OUTPUTS", pasta)
    monkeypatch.setattr(modulo_log, "ARQUIVO_HISTORICO", arquivo)

    modulo_log.registrar_log(
        status_execucao="SUCESSO",
        mensagem_erro=""
    )

    modulo_log.registrar_log(
        status_execucao="ERRO",
        mensagem_erro="Falha simulada"
    )

    with open(arquivo, newline="", encoding="utf-8") as arquivo_csv:
        registros = list(csv.DictReader(arquivo_csv))

    assert len(registros) == 2
    assert registros[0]["status_execucao"] == "SUCESSO"
    assert registros[1]["status_execucao"] == "ERRO"
    assert registros[1]["mensagem_erro"] == "Falha simulada"
