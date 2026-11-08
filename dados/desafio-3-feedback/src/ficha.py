
from pathlib import Path
import pandas as pd

from src.indicadores import calcular_indicadores
from src.contexto import gerar_alertas


PASTA_DADOS = Path(__file__).resolve().parent.parent

COLUNAS_INDICADORES = [
    "valor_vendido",
    "vendas",
    "pecas",
    "atendimentos",
    "ticket_medio",
    "pa",
    "conversao",
    "meta_valor",
    "atingimento",
]


def converter_para_dict(linha):
    """Transforma os indicadores em um dicionário compatível com JSON."""

    resultado = {}

    for coluna in COLUNAS_INDICADORES:
        if coluna not in linha.index:
            continue

        valor = linha[coluna]

        if pd.isna(valor):
            resultado[coluna] = None
        elif coluna in ["vendas", "pecas", "atendimentos"]:
            resultado[coluna] = int(valor)
        else:
            resultado[coluna] = float(valor)

    return resultado


def gerar_ficha(vendedor_id, mes):
    """
    Monta a ficha de contexto de um vendedor.

    Exemplo:
    gerar_ficha("C0036", "2026-09")
    """

    vendedores, loja = calcular_indicadores()

    vendedor = vendedores[
        (vendedores["vendedor_id"] == vendedor_id)
        & (vendedores["mes"] == mes)
    ]

    if vendedor.empty:
        raise ValueError(
            "Não existem indicadores para esse vendedor e mês."
        )

    linha_atual = vendedor.iloc[0]
    nome = linha_atual["nome"]

    # Identifica o mês anterior
    mes_anterior = (
        pd.Period(mes, freq="M") - 1
    ).strftime("%Y-%m")

    # Indicadores do mês atual
    indicadores_mes = converter_para_dict(linha_atual)

    # Indicadores do mês anterior
    anterior = vendedores[
        (vendedores["vendedor_id"] == vendedor_id)
        & (vendedores["mes"] == mes_anterior)
    ]

    if anterior.empty:
        indicadores_mes_anterior = None
    else:
        indicadores_mes_anterior = converter_para_dict(
            anterior.iloc[0]
        )

    # Indicadores gerais da loja no mês atual
    dados_loja = loja[loja["mes"] == mes]

    if dados_loja.empty:
        indicadores_loja = None
    else:
        indicadores_loja = converter_para_dict(
            dados_loja.iloc[0]
        )

    # Alertas identificados na Etapa 4
    alertas = gerar_alertas(vendedor_id, mes)

    # Carrega as anotações gerenciais
    anotacoes = pd.read_csv(
        PASTA_DADOS / "anotacoes_gerente.csv",
        keep_default_na=False
    )

    anotacoes["data"] = pd.to_datetime(anotacoes["data"])

    anotacoes_mes = anotacoes[
        (anotacoes["sobre"] == nome)
        & (anotacoes["data"].dt.strftime("%Y-%m") == mes)
    ].copy()

    # Identifica quais anotações foram marcadas como sensíveis
    sensiveis = pd.read_csv(
        PASTA_DADOS / "saidas" / "sensiveis.csv",
        keep_default_na=False
    )

    sensiveis["data"] = pd.to_datetime(sensiveis["data"])

    # Remove as anotações sensíveis antes de montar a ficha
    anotacoes_mes = anotacoes_mes.merge(
        sensiveis[["data", "sobre", "sensivel"]],
        on=["data", "sobre"],
        how="left"
    )

    anotacoes_mes["sensivel"] = (
        anotacoes_mes["sensivel"]
        .fillna("False")
        .astype(str)
        .str.lower()
    )

    anotacoes_mes = anotacoes_mes[
        anotacoes_mes["sensivel"] != "true"
    ]

    lista_anotacoes = []

    for _, anotacao in anotacoes_mes.iterrows():
        lista_anotacoes.append({
            "data": anotacao["data"].strftime("%Y-%m-%d"),
            "anotacao": anotacao["anotacao"]
        })

    # Monta a ficha completa
    ficha = {
        "vendedor": {
            "id": vendedor_id,
            "nome": nome
        },
        "mes_analisado": mes,
        "indicadores_mes": indicadores_mes,
        "indicadores_mes_anterior": indicadores_mes_anterior,
        "indicadores_loja": indicadores_loja,
        "alertas_contexto": alertas,
        "anotacoes_gerente": lista_anotacoes
    }

    return ficha
