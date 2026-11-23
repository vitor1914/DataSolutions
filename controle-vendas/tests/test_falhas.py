import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import executar_pipeline as modulo_pipeline


def test_pipeline_registra_falha_na_importacao(monkeypatch):
    """Deve registrar o erro e interromper o pipeline."""

    registros = []

    def simular_falha():
        raise RuntimeError("Falha simulada na importação")

    def registrar_log_teste(
        importados,
        validos,
        pendentes,
        aprovados,
        status,
        resultado,
        mensagem
    ):
        registros.append({
            "resultado": resultado,
            "mensagem": mensagem
        })

    monkeypatch.setattr(
        modulo_pipeline,
        "importar_dados",
        simular_falha
    )

    monkeypatch.setattr(
        modulo_pipeline,
        "registrar_log",
        registrar_log_teste
    )

    with pytest.raises(
        RuntimeError,
        match="Falha simulada na importação"
    ):
        modulo_pipeline.executar_pipeline()

    assert len(registros) == 1
    assert registros[0]["resultado"] == "ERRO"
    assert "Falha simulada na importação" in registros[0]["mensagem"]


def test_falha_preserva_base_original(monkeypatch):
    """Uma falha no pipeline não deve alterar a base original."""

    import hashlib

    arquivo = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "vendas_brutas.csv"
    )

    hash_antes = hashlib.sha256(arquivo.read_bytes()).hexdigest()

    def simular_falha():
        raise RuntimeError("Falha para testar preservação")

    monkeypatch.setattr(
        modulo_pipeline,
        "importar_dados",
        simular_falha
    )

    monkeypatch.setattr(
        modulo_pipeline,
        "registrar_log",
        lambda *args: None
    )

    with pytest.raises(RuntimeError):
        modulo_pipeline.executar_pipeline()

    hash_depois = hashlib.sha256(arquivo.read_bytes()).hexdigest()

    assert hash_antes == hash_depois
    assert hash_antes == (
        "96e1696ec8bfc71650b3991a9a3589d1c2d92789c8d05d71debe8e4a6ed70ffd"
    )
