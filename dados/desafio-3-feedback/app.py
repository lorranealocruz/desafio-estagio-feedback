
import streamlit as st
from src.indicadores import calcular_indicadores


def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# Configuração da página
st.set_page_config(
    page_title="Feedback FullStore",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Indicadores de Desempenho")
st.caption("Desafio 3 — Feedback FullStore")

# Carrega os indicadores
try:
    vendedores, loja = calcular_indicadores()

except Exception as erro:
    st.error(f"Erro ao carregar os dados: {erro}")
    st.stop()


# Seleção do mês
meses = sorted(loja["mes"].unique(), reverse=True)

mes_selecionado = st.selectbox(
    "Selecione o mês:",
    meses
)


# Dados gerais da loja
dados_loja = loja[
    loja["mes"] == mes_selecionado
].iloc[0]


st.subheader("Resultado geral da loja")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Faturamento",
    moeda(dados_loja["valor_vendido"])
)

col2.metric(
    "Meta",
    moeda(dados_loja["meta_valor"])
)

col3.metric(
    "Atingimento",
    f"{dados_loja['atingimento']:.2%}"
)


st.divider()

# Dados individuais
st.subheader("Desempenho dos vendedores")

dados_vendedores = vendedores[
    vendedores["mes"] == mes_selecionado
].copy()

dados_exibicao = dados_vendedores[
    [
        "nome",
        "valor_vendido",
        "ticket_medio",
        "pa",
        "conversao",
        "atingimento"
    ]
].copy()

dados_exibicao = dados_exibicao.rename(
    columns={
        "nome": "Vendedor",
        "valor_vendido": "Faturamento",
        "ticket_medio": "Ticket médio",
        "pa": "P.A.",
        "conversao": "Conversão",
        "atingimento": "Atingimento"
    }
)

st.dataframe(
    dados_exibicao,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Os indicadores são calculados em Python com Pandas. "
    "A inteligência artificial não participa dos cálculos."
)
