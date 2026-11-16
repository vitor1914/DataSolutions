
from pathlib import Path
import pandas as pd

from importar_dados import importar_dados


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_TRATADO = BASE_DIR / "data" / "vendas_tratadas.csv"
ARQUIVO_PENDENTE = BASE_DIR / "outputs" / "registros_pendentes.csv"


def identificar_pendencias(df):
    """Identifica os registros que precisam de análise manual."""

    motivos = pd.Series("", index=df.index, dtype="object")

    def adicionar_motivo(condicao, descricao):
        """Adiciona um motivo sem sobrescrever os anteriores."""
        for indice in df.index[condicao]:
            if motivos[indice]:
                motivos[indice] += "; " + descricao
            else:
                motivos[indice] = descricao

    # 1. Identificadores ausentes
    ids_ausentes = df["id_venda"].isna()

    adicionar_motivo(
        ids_ausentes,
        "ID da venda ausente"
    )

    # 2. Identificadores repetidos
    ids_repetidos = df.duplicated(
        subset=["id_venda"],
        keep=False
    ) & df["id_venda"].notna()

    adicionar_motivo(
        ids_repetidos,
        "ID da venda repetido"
    )

    # 3. Registros totalmente duplicados
    duplicados = df.duplicated(keep=False)

    adicionar_motivo(
        duplicados,
        "Registro totalmente duplicado"
    )

    # 4. Datas ausentes ou inválidas
    datas = pd.to_datetime(
        df["data_venda"],
        errors="coerce"
    )

    adicionar_motivo(
        df["data_venda"].isna(),
        "Data da venda ausente"
    )

    adicionar_motivo(
        df["data_venda"].notna() & datas.isna(),
        "Data da venda inválida"
    )

    # 5. Quantidade
    quantidade = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    adicionar_motivo(
        quantidade.isna(),
        "Quantidade ausente ou não numérica"
    )

    adicionar_motivo(
        quantidade.notna() & (quantidade <= 0),
        "Quantidade menor ou igual a zero"
    )

    # 6. Preço unitário
    preco = pd.to_numeric(
        df["preco_unitario"],
        errors="coerce"
    )

    adicionar_motivo(
        preco.isna(),
        "Preço unitário ausente ou não numérico"
    )

    adicionar_motivo(
        preco.notna() & (preco <= 0),
        "Preço unitário menor ou igual a zero"
    )

    # 7. Campos obrigatórios
    campos_obrigatorios = [
        "produto",
        "categoria",
        "vendedor",
        "regiao"
    ]

    for coluna in campos_obrigatorios:
        vazios = (
            df[coluna].isna()
            | df[coluna].astype("string").str.strip().eq("").fillna(False)
        )

        adicionar_motivo(
            vazios,
            f"Campo obrigatório ausente: {coluna}"
        )

    return motivos


def tratar_dados(df):
    """Separa registros válidos dos registros pendentes."""

    motivos = identificar_pendencias(df)

    # Registros sem inconsistências
    validos = df.loc[motivos.eq("")].copy()

    # Registros que precisam de análise manual
    pendentes = df.loc[motivos.ne("")].copy()

    # Converte os tipos de dados da base tratada
    validos["data_venda"] = pd.to_datetime(
        validos["data_venda"],
        errors="raise"
    )

    validos["quantidade"] = pd.to_numeric(
        validos["quantidade"],
        errors="raise"
    )

    validos["preco_unitario"] = pd.to_numeric(
        validos["preco_unitario"],
        errors="raise"
    )

    # Informações para rastrear os registros pendentes
    pendentes.insert(
        0,
        "linha_origem",
        pendentes.index + 2
    )

    pendentes["motivo_pendencia"] = motivos.loc[
        pendentes.index
    ].values

    # Cria os diretórios, caso não existam
    ARQUIVO_TRATADO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ARQUIVO_PENDENTE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Salva os arquivos sem modificar a base original
    validos.to_csv(
        ARQUIVO_TRATADO,
        index=False,
        encoding="utf-8-sig"
    )

    pendentes.to_csv(
        ARQUIVO_PENDENTE,
        index=False,
        encoding="utf-8-sig"
    )

    return validos, pendentes


def main():
    print("=" * 60)
    print("DATASOLUTIONS - TRATAMENTO DE DADOS")
    print("=" * 60)

    df = importar_dados()

    validos, pendentes = tratar_dados(df)

    print("\nRESULTADO DO TRATAMENTO")
    print("-" * 60)

    print(f"Registros originais: {len(df)}")
    print(f"Registros tratados: {len(validos)}")
    print(f"Registros pendentes: {len(pendentes)}")

    print("\nARQUIVOS GERADOS")
    print("-" * 60)

    print(f"Base tratada: {ARQUIVO_TRATADO}")
    print(f"Registros pendentes: {ARQUIVO_PENDENTE}")

    print("\nNenhum registro foi excluído da base original.")

    print("\n" + "=" * 60)
    print("TRATAMENTO FINALIZADO")
    print("=" * 60)


if __name__ == "__main__":
    main()
