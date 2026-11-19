
import csv
from datetime import datetime
from pathlib import Path


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_OUTPUTS = BASE_DIR / "outputs"

ARQUIVO_HISTORICO = (
    PASTA_OUTPUTS / "historico_execucoes.csv"
)


# Estrutura das colunas
CAMPOS = [
    "data_execucao",
    "hora_execucao",
    "registros_importados",
    "registros_validos",
    "registros_pendentes",
    "registros_aprovados",
    "status_validacao",
    "status_execucao",
    "mensagem_erro"
]


def registrar_log(
    registros_importados=0,
    registros_validos=0,
    registros_pendentes=0,
    registros_aprovados=0,
    status_validacao="REPROVADA",
    status_execucao="ERRO",
    mensagem_erro=""
):
    """
    Registra uma execução no histórico CSV.
    Preserva os registros anteriores.
    """

    # Criar pasta outputs, se necessário
    PASTA_OUTPUTS.mkdir(
        parents=True,
        exist_ok=True
    )

    # Data e horário da execução
    agora = datetime.now()

    # Novo registro
    registro = {
        "data_execucao": agora.strftime("%d/%m/%Y"),
        "hora_execucao": agora.strftime("%H:%M:%S"),
        "registros_importados": registros_importados,
        "registros_validos": registros_validos,
        "registros_pendentes": registros_pendentes,
        "registros_aprovados": registros_aprovados,
        "status_validacao": status_validacao,
        "status_execucao": status_execucao,
        "mensagem_erro": mensagem_erro
    }

    # Verificar se o histórico já existe
    arquivo_existe = ARQUIVO_HISTORICO.exists()

    # Modo append: adiciona sem apagar os dados anteriores
    with open(
        ARQUIVO_HISTORICO,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS
        )

        # Criar cabeçalho somente na primeira execução
        if not arquivo_existe or ARQUIVO_HISTORICO.stat().st_size == 0:
            escritor.writeheader()

        escritor.writerow(registro)

    print("\nRegistro de execução salvo no histórico.")
