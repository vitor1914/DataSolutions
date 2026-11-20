from pathlib import Path
from datetime import datetime

import pandas as pd


def auditar_dados(df, resultados):
    """Audita a qualidade dos dados sem modificar a base original."""

    identificadores = resultados["identificadores"]
    datas = resultados["datas"]
    comercial = resultados["comercial"]

    total = len(df)

    # Identificação das ocorrências
    ocorrencias = {
        "id_ausente": identificadores["ids_ausentes"],
        "id_repetido": len(identificadores["ids_repetidos"]),
        "linha_duplicada": len(identificadores["linhas_duplicadas"]),
        "data_ausente": datas["datas_ausentes"],
        "data_invalida": datas["datas_invalidas"],
        "quantidade_ausente": comercial["quantidade"]["ausentes"],
        "quantidade_invalida": comercial["quantidade"]["invalidos"],
        "preco_ausente": comercial["preco_unitario"]["ausentes"],
        "preco_invalido": comercial["preco_unitario"]["invalidos"],
        "produto_ausente": comercial["produto"]["ausentes"],
        "categoria_ausente": comercial["categoria"]["ausentes"],
        "vendedor_ausente": comercial["vendedor"]["ausentes"],
        "regiao_ausente": comercial["regiao"]["ausentes"]
    }

    # Identificação dos registros reprovados
    reprovados = pd.Series(False, index=df.index)

    reprovados |= df["id_venda"].isna()
    reprovados |= df.duplicated(
        subset=["id_venda"], keep=False
    )
    reprovados |= df.duplicated(keep=False)

    reprovados |= datas["datas_convertidas"].isna()

    quantidade = pd.to_numeric(
        df["quantidade"], errors="coerce"
    )
    reprovados |= quantidade.isna() | (quantidade <= 0)

    preco = pd.to_numeric(
        df["preco_unitario"], errors="coerce"
    )
    reprovados |= preco.isna() | (preco <= 0)

    for coluna in ["produto", "categoria", "vendedor", "regiao"]:
        vazio = (
            df[coluna].isna()
            | df[coluna].astype("string").str.strip().eq("").fillna(False)
        )
        reprovados |= vazio

    total_reprovados = int(reprovados.sum())
    total_aprovados = total - total_reprovados

    taxa_aprovacao = (
        total_aprovados / total * 100 if total else 0
    )

    taxa_reprovacao = (
        total_reprovados / total * 100 if total else 0
    )

    return {
        "total_registros": total,
        "registros_aprovados": total_aprovados,
        "registros_reprovados": total_reprovados,
        "taxa_aprovacao": taxa_aprovacao,
        "taxa_reprovacao": taxa_reprovacao,
        "ocorrencias": ocorrencias,
        "registros_reprovados_detalhe": df.loc[reprovados].copy()
    }


def gerar_relatorio_auditoria(auditoria, caminho):
    """Gera o relatório de auditoria em arquivo TXT."""

    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    ocorrencias = auditoria["ocorrencias"]

    linhas = [
        "=" * 60,
        "DATASOLUTIONS - RELATORIO DE AUDITORIA",
        "=" * 60,
        "",
        f"Data da auditoria: {datetime.now():%d/%m/%Y %H:%M:%S}",
        "",
        "1. INDICADORES GERAIS",
        "-" * 60,
        f"Total de registros: {auditoria['total_registros']}",
        f"Registros aprovados: {auditoria['registros_aprovados']}",
        f"Registros reprovados: {auditoria['registros_reprovados']}",
        f"Taxa de aprovacao: {auditoria['taxa_aprovacao']:.2f}%",
        f"Taxa de reprovacao: {auditoria['taxa_reprovacao']:.2f}%",
        "",
        "2. OCORRENCIAS POR CATEGORIA",
        "-" * 60
    ]

    for categoria, quantidade in ocorrencias.items():
        linhas.append(f"{categoria}: {quantidade}")

    linhas.extend([
        "",
        "3. RESULTADO DA AUDITORIA",
        "-" * 60,
        "Auditoria concluida.",
        "Base original preservada.",
        "",
        "=" * 60
    ])

    caminho.write_text(
        "\n".join(linhas) + "\n",
        encoding="utf-8"
    )

    return caminho
