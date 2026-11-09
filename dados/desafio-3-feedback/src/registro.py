import csv
from datetime import datetime
from pathlib import Path


# Localiza a pasta principal do projeto
PASTA_DADOS = Path(__file__).resolve().parent.parent

# Define onde os feedbacks aprovados serão armazenados
PASTA_SAIDAS = PASTA_DADOS / "saidas"

ARQUIVO_FEEDBACKS = PASTA_SAIDAS / "feedbacks_aprovados.csv"


def salvar_feedback_aprovado(ficha, texto_feedback, caminho_arquivo=None):
    """
    Salva o feedback aprovado em um arquivo CSV.
    """

    # Permite utilizar outro arquivo durante os testes
    if caminho_arquivo is None:
        caminho_arquivo = ARQUIVO_FEEDBACKS

    caminho_arquivo = Path(caminho_arquivo)

    # Garante que a pasta de destino exista
    caminho_arquivo.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Prepara os dados do registro
    registro = {
        "data_aprovacao": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "vendedor_id": ficha["vendedor"]["id"],
        "vendedor_nome": ficha["vendedor"]["nome"],
        "mes_referencia": ficha["mes_analisado"],
        "feedback": texto_feedback
    }

    colunas = [
        "data_aprovacao",
        "vendedor_id",
        "vendedor_nome",
        "mes_referencia",
        "feedback"
    ]

    # Verifica se o arquivo precisa receber o cabeçalho
    precisa_cabecalho = (
        not caminho_arquivo.exists()
        or caminho_arquivo.stat().st_size == 0
    )

    # Acrescenta o registro sem apagar os anteriores
    with open(
        caminho_arquivo,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        if precisa_cabecalho:
            escritor.writeheader()

        escritor.writerow(registro)

    return caminho_arquivo
