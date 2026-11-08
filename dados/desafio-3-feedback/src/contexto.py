
from pathlib import Path
import pandas as pd


# Localiza a pasta principal do desafio
PASTA_DADOS = Path(__file__).resolve().parent.parent


def carregar_contextos():
    """Carrega os arquivos necessários para identificar os contextos."""

    vendedores = pd.read_csv(
        PASTA_DADOS / "vendedores.csv",
        keep_default_na=False
    )

    diario = pd.read_csv(
        PASTA_DADOS / "indicadores_diarios_vendedor.csv"
    )

    anotacoes = pd.read_csv(
        PASTA_DADOS / "anotacoes_gerente.csv",
        keep_default_na=False
    )

    sensiveis = pd.read_csv(
        PASTA_DADOS / "saidas" / "sensiveis.csv",
        keep_default_na=False
    )

    # Padroniza as datas para facilitar as comparações
    diario["data"] = pd.to_datetime(diario["data"])
    anotacoes["data"] = pd.to_datetime(anotacoes["data"])
    sensiveis["data"] = pd.to_datetime(sensiveis["data"])

    diario["vendas"] = pd.to_numeric(
        diario["vendas"],
        errors="raise"
    )

    return vendedores, diario, anotacoes, sensiveis


def verificar_ferias(vendedor, mes):
    """Verifica se o vendedor teve férias durante o mês analisado."""

    ferias = vendedor["ferias_no_periodo"]

    if not ferias:
        return None

    try:
        inicio, fim = [
            pd.to_datetime(data.strip())
            for data in ferias.split(" a ")
        ]
    except ValueError:
        return None

    inicio_mes = pd.Timestamp(f"{mes}-01")
    fim_mes = inicio_mes + pd.offsets.MonthEnd(0)

    # Verifica se o período de férias cruza o mês analisado
    if inicio <= fim_mes and fim >= inicio_mes:
        return (
            f"Teve férias entre {inicio.strftime('%d/%m/%Y')} "
            f"e {fim.strftime('%d/%m/%Y')} no período analisado."
        )

    return None


def gerar_alertas(vendedor_id, mes):
    """
    Gera alertas de contexto para um vendedor em determinado mês.

    Exemplo:
    gerar_alertas("C0036", "2026-09")
    """

    vendedores, diario, anotacoes, sensiveis = carregar_contextos()

    vendedor_encontrado = vendedores[
        vendedores["vendedor_id"] == vendedor_id
    ]

    if vendedor_encontrado.empty:
        raise ValueError("Vendedor não encontrado.")

    vendedor = vendedor_encontrado.iloc[0]
    nome = vendedor["nome"]

    alertas = []

    # 1. Verifica férias
    alerta_ferias = verificar_ferias(vendedor, mes)

    if alerta_ferias:
        alertas.append(alerta_ferias)

    # 2. Verifica tempo de admissão
    admissao = pd.to_datetime(vendedor["data_admissao"])
    fim_mes = pd.Timestamp(f"{mes}-01") + pd.offsets.MonthEnd(0)

    dias_empresa = (fim_mes - admissao).days

    if 0 <= dias_empresa < 90:
        alertas.append(
            f"Estava com menos de 90 dias de empresa ao final de {mes}."
        )

    # 3. Verifica escala de trabalho
    if vendedor["escala"] != "6x1":
        alertas.append(
            f"Trabalha na escala {vendedor['escala']}, diferente da escala 6x1."
        )

    # Filtra os registros do vendedor no mês
    dados_mes = diario[
        (diario["vendedor_id"] == vendedor_id)
        & (diario["data"].dt.strftime("%Y-%m") == mes)
    ]

    # Conta datas distintas em que houve pelo menos uma venda
    dias_com_venda = dados_mes.loc[
        dados_mes["vendas"] > 0,
        "data"
    ].dt.date.nunique()

    # 4. Verifica se teve menos de 10 dias com vendas
    if dias_com_venda < 10:
        alertas.append(
            f"Teve vendas em apenas {dias_com_venda} dias no mês. "
            "Considere o contexto antes de interpretar esse indicador."
        )

    # 5. Identifica anotações sensíveis sem expor seu conteúdo
    anotacoes_sensiveis = sensiveis[
        (sensiveis["sobre"] == nome)
        & (sensiveis["data"].dt.strftime("%Y-%m") == mes)
        & (sensiveis["sensivel"].astype(str).str.lower() == "true")
    ]

    for _, anotacao in anotacoes_sensiveis.iterrows():
        data = anotacao["data"].strftime("%d/%m/%Y")

        alertas.append(
            f"Existe uma anotação gerencial marcada como sensível "
            f"em {data}. Não utilize seu conteúdo como cobrança "
            "no feedback."
        )

    return alertas
