
import sys
from pathlib import Path

import pandas as pd
import pytest

# Permite importar os módulos existentes da pasta src
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from validar_dados import validar_dados


@pytest.fixture
def base_valida():
    """Cria uma pequena base fictícia sem inconsistências."""

    return pd.DataFrame({
        "id_venda": [1, 2],
        "data_venda": ["2026-10-01", "2026-10-02"],
        "produto": ["Notebook", "Mouse"],
        "categoria": ["Eletronicos", "Perifericos"],
        "quantidade": [2, 5],
        "preco_unitario": [3500.0, 80.0],
        "vendedor": ["Joao", "Maria"],
        "regiao": ["Sudeste", "Sul"]
    })


def test_identificar_id_duplicado(base_valida):
    """Deve identificar IDs repetidos."""

    base_valida.loc[1, "id_venda"] = 1

    resultado = validar_dados(base_valida)

    repetidos = resultado["identificadores"]["ids_repetidos"]

    assert len(repetidos) == 2


def test_identificar_id_ausente(base_valida):
    """Deve identificar ID ausente."""

    base_valida.loc[0, "id_venda"] = None

    resultado = validar_dados(base_valida)

    assert resultado["identificadores"]["ids_ausentes"] == 1


def test_identificar_data_invalida(base_valida):
    """Deve identificar data inválida."""

    base_valida.loc[0, "data_venda"] = "data_invalida"

    resultado = validar_dados(base_valida)

    assert resultado["datas"]["datas_invalidas"] == 1


def test_identificar_quantidade_negativa(base_valida):
    """Deve identificar quantidade negativa."""

    base_valida.loc[0, "quantidade"] = -2

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["quantidade"]["invalidos"] == 1


def test_identificar_quantidade_zero(base_valida):
    """Deve identificar quantidade igual a zero."""

    base_valida.loc[0, "quantidade"] = 0

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["quantidade"]["invalidos"] == 1


def test_identificar_preco_zero(base_valida):
    """Deve identificar preço igual a zero."""

    base_valida.loc[0, "preco_unitario"] = 0

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["preco_unitario"]["invalidos"] == 1


def test_identificar_preco_ausente(base_valida):
    """Deve identificar preço ausente."""

    base_valida.loc[0, "preco_unitario"] = None

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["preco_unitario"]["ausentes"] == 1


def test_identificar_produto_vazio(base_valida):
    """Deve identificar produto vazio."""

    base_valida.loc[0, "produto"] = "   "

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["produto"]["ausentes"] == 1


def test_aprovar_base_valida(base_valida):
    """Uma base válida não deve apresentar inconsistências."""

    resultado = validar_dados(base_valida)

    assert resultado["identificadores"]["ids_ausentes"] == 0
    assert resultado["identificadores"]["ids_repetidos"].empty
    assert resultado["identificadores"]["total_linhas_duplicadas"] == 0

    assert resultado["datas"]["datas_ausentes"] == 0
    assert resultado["datas"]["datas_invalidas"] == 0

    assert resultado["comercial"]["quantidade"]["ausentes"] == 0
    assert resultado["comercial"]["quantidade"]["invalidos"] == 0

    assert resultado["comercial"]["preco_unitario"]["ausentes"] == 0
    assert resultado["comercial"]["preco_unitario"]["invalidos"] == 0

    for coluna in ["produto", "categoria", "vendedor", "regiao"]:
        assert resultado["comercial"][coluna]["ausentes"] == 0


def test_coluna_obrigatoria_ausente():
    """Deve gerar erro quando uma coluna obrigatória não existir."""

    import pandas as pd
    import pytest
    from validar_dados import validar_dados

    df = pd.DataFrame({
        "id_venda": [101],
        "produto": ["Notebook"],
        "categoria": ["Eletrônicos"],
        "quantidade": [2],
        "preco_unitario": [3500.0],
        "vendedor": ["João"],
        "regiao": ["Sudeste"]
    })

    with pytest.raises(KeyError):
        validar_dados(df)


def test_identificar_quantidade_ausente(base_valida):
    """Deve identificar quantidade ausente."""

    base_valida.loc[0, "quantidade"] = None

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["quantidade"]["ausentes"] == 1


def test_identificar_preco_negativo(base_valida):
    """Deve identificar preço negativo."""

    base_valida.loc[0, "preco_unitario"] = -10

    resultado = validar_dados(base_valida)

    assert resultado["comercial"]["preco_unitario"]["invalidos"] == 1


@pytest.mark.parametrize("coluna", [
    "categoria",
    "vendedor",
    "regiao"
])
def test_identificar_campo_obrigatorio_vazio(base_valida, coluna):
    """Deve identificar campos obrigatórios vazios."""

    base_valida.loc[0, coluna] = "   "

    resultado = validar_dados(base_valida)

    assert resultado["comercial"][coluna]["ausentes"] == 1
