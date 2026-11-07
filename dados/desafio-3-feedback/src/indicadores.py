
from pathlib import Path
import pandas as pd


# Caminho da pasta onde estão os arquivos CSV
PASTA_DADOS = Path(__file__).resolve().parent.parent

# Período que será analisado
MESES_ANALISE = ["2026-08", "2026-09", "2026-10"]

# Colunas que serão somadas
COLUNAS_SOMA = [
    "valor_vendido",
    "vendas",
    "pecas",
    "atendimentos"
]


def carregar_dados():
    """
    Lê os arquivos CSV e prepara os dados.
    """

    diario = pd.read_csv(
        PASTA_DADOS / "indicadores_diarios_vendedor.csv"
    )

    metas_vendedor = pd.read_csv(
        PASTA_DADOS / "metas_vendedor.csv"
    )

    metas_loja = pd.read_csv(
        PASTA_DADOS / "metas_loja.csv"
    )

    # Converte a coluna de data para formato datetime
    diario["data"] = pd.to_datetime(
        diario["data"],
        errors="coerce"
    )

    if diario["data"].isna().any():
        raise ValueError("Existem datas inválidas no CSV.")

    # Garante que as colunas numéricas sejam números
    for coluna in COLUNAS_SOMA:
        diario[coluna] = pd.to_numeric(
            diario[coluna],
            errors="raise"
        )

    # Cria uma coluna com ano e mês
    diario["mes"] = diario["data"].dt.strftime("%Y-%m")

    # Considera somente agosto, setembro e outubro
    diario = diario[
        diario["mes"].isin(MESES_ANALISE)
    ].copy()

    # Prepara as metas para o cruzamento
    metas_vendedor["mes"] = (
        metas_vendedor["mes"].astype(str)
    )

    metas_loja["mes"] = (
        metas_loja["mes"].astype(str)
    )

    return diario, metas_vendedor, metas_loja


def adicionar_indicadores(df):
    """
    Calcula os indicadores usando os totais agrupados.
    """

    df = df.copy()

    # Ticket médio = faturamento / vendas
    df["ticket_medio"] = (
        df["valor_vendido"]
        .div(df["vendas"])
        .where(df["vendas"].ne(0))
    )

    # P.A. = peças / vendas
    df["pa"] = (
        df["pecas"]
        .div(df["vendas"])
        .where(df["vendas"].ne(0))
    )

    # Conversão = vendas / atendimentos
    df["conversao"] = (
        df["vendas"]
        .div(df["atendimentos"])
        .where(df["atendimentos"].ne(0))
    )

    # Atingimento = faturamento / meta
    if "meta_valor" in df.columns:
        df["atingimento"] = (
            df["valor_vendido"]
            .div(df["meta_valor"])
            .where(
                df["meta_valor"].notna()
                & df["meta_valor"].ne(0)
            )
        )

    return df


def calcular_indicadores():
    """
    Consolida os dados individuais e da loja.
    """

    diario, metas_vendedor, metas_loja = (
        carregar_dados()
    )

    # Agrupamento por vendedor e mês
    vendedores = (
        diario
        .groupby(
            ["mes", "vendedor_id", "nome"],
            as_index=False
        )[COLUNAS_SOMA]
        .sum()
    )

    # Adiciona as metas individuais
    vendedores = vendedores.merge(
        metas_vendedor[
            ["vendedor_id", "mes", "meta_valor"]
        ],
        on=["vendedor_id", "mes"],
        how="left",
        validate="one_to_one"
    )

    vendedores = adicionar_indicadores(vendedores)

    # Agrupamento geral da loja por mês
    loja = (
        diario
        .groupby("mes", as_index=False)[COLUNAS_SOMA]
        .sum()
    )

    # Adiciona as metas gerais da loja
    loja = loja.merge(
        metas_loja[["mes", "meta_valor"]],
        on="mes",
        how="left",
        validate="one_to_one"
    )

    loja = adicionar_indicadores(loja)

    # Organiza os resultados
    vendedores = vendedores.sort_values(
        ["mes", "nome"]
    )

    loja = loja.sort_values("mes")

    return vendedores, loja
