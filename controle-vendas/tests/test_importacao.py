import sys
from pathlib import Path

import pandas as pd
import pytest

# Permite importar os módulos da pasta src
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import importar_dados as modulo_importacao


def test_importar_csv_valido(tmp_path, monkeypatch):
    """Deve importar corretamente um CSV válido."""

    arquivo = tmp_path / "vendas_teste.csv"

    dados = pd.DataFrame({
        "id_venda": [101, 102],
        "data_venda": ["2026-11-01", "2026-11-02"],
        "produto": ["Notebook", "Mouse"],
        "categoria": ["Eletronicos", "Perifericos"],
        "quantidade": [2, 5],
        "preco_unitario": [3500.0, 80.0],
        "vendedor": ["Joao", "Maria"],
        "regiao": ["Sudeste", "Sul"]
    })

    dados.to_csv(arquivo, index=False)

    # Redireciona o importador para o arquivo temporário
    monkeypatch.setattr(
        modulo_importacao,
        "ARQUIVO_DADOS",
        arquivo
    )

    resultado = modulo_importacao.importar_dados()

    assert len(resultado) == 2
    assert len(resultado.columns) == 8
    assert resultado["id_venda"].tolist() == [101, 102]
    assert resultado["produto"].tolist() == ["Notebook", "Mouse"]


def test_arquivo_inexistente(tmp_path, monkeypatch):
    """Deve informar erro quando o CSV não existir."""

    arquivo = tmp_path / "arquivo_inexistente.csv"

    monkeypatch.setattr(
        modulo_importacao,
        "ARQUIVO_DADOS",
        arquivo
    )

    with pytest.raises(FileNotFoundError, match="Arquivo não encontrado"):
        modulo_importacao.importar_dados()


def test_arquivo_vazio(tmp_path, monkeypatch):
    """Deve identificar um CSV vazio."""

    arquivo = tmp_path / "vendas_vazio.csv"
    arquivo.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        modulo_importacao,
        "ARQUIVO_DADOS",
        arquivo
    )

    with pytest.raises(pd.errors.EmptyDataError):
        modulo_importacao.importar_dados()


def test_coluna_id_venda_ausente(tmp_path, monkeypatch):
    """Deve identificar a ausência da coluna id_venda."""

    arquivo = tmp_path / "vendas_sem_id.csv"

    arquivo.write_text(
        "produto,quantidade\nNotebook,2\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        modulo_importacao,
        "ARQUIVO_DADOS",
        arquivo
    )

    with pytest.raises(KeyError):
        modulo_importacao.importar_dados()
