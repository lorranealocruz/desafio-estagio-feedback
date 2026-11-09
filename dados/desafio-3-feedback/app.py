import streamlit as st

from src.indicadores import calcular_indicadores
from src.ficha import gerar_ficha
from src.ia import gerar_feedback
from src.registro import salvar_feedback_aprovado
from src.validacao import (
    validar_numeros,
    validar_associacoes,
    validar_referencias_completas
)


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


st.divider()


# Seleção do vendedor para gerar feedback
st.subheader("Feedback individual")

opcoes_vendedores = dados_vendedores[
    ["vendedor_id", "nome"]
].drop_duplicates()

nome_selecionado = st.selectbox(
    "Selecione o vendedor para analisar:",
    opcoes_vendedores["nome"].tolist()
)


# Recupera o ID correspondente ao nome selecionado
vendedor_selecionado = opcoes_vendedores[
    opcoes_vendedores["nome"] == nome_selecionado
].iloc[0]

vendedor_id = vendedor_selecionado["vendedor_id"]


# Identifica a ficha atualmente selecionada
contexto_atual = (vendedor_id, mes_selecionado)

# Limpa o feedback anterior caso o vendedor ou mês mude
if st.session_state.get("feedback_contexto") != contexto_atual:

    st.session_state.pop("feedback_gerado", None)
    st.session_state.pop("feedback_editavel", None)
    st.session_state.pop("feedback_salvo_texto", None)

    st.session_state["feedback_contexto"] = contexto_atual


# Gera a ficha de contexto
try:

    ficha = gerar_ficha(
        vendedor_id,
        mes_selecionado
    )

    st.success("Ficha de contexto carregada!")

    st.write("**Alertas de contexto**")

    if ficha["alertas_contexto"]:

        for alerta in ficha["alertas_contexto"]:
            st.warning(alerta)

    else:
        st.info("Nenhum alerta de contexto identificado.")


    st.write("**Anotações do gerente**")

    if ficha["anotacoes_gerente"]:

        for anotacao in ficha["anotacoes_gerente"]:

            st.write(
                f"- {anotacao['data']}: "
                f"{anotacao['anotacao']}"
            )

    else:
        st.info("Nenhuma anotação disponível para esse mês.")


    st.divider()

    st.subheader("Feedback individual com inteligência artificial")


    # Geração do feedback
    if st.button("Gerar feedback com IA"):

        with st.spinner(
            "A inteligência artificial está elaborando o feedback..."
        ):

            feedback = gerar_feedback(ficha)

            st.session_state["feedback_gerado"] = feedback

            st.session_state["feedback_editavel"] = "\n\n".join([
                f"Cuidados: {feedback['cuidados']}",
                f"Abertura: {feedback['abertura']}",
                f"Ponto forte: {feedback['ponto_forte']}",
                f"Ponto a melhorar: {feedback['ponto_a_melhorar']}",
                f"Pergunta aberta: {feedback['pergunta_aberta']}",
                f"Combinado para a semana: {feedback['combinado_para_a_semana']}",
                f"Acompanhamento: {feedback['acompanhamento']}",
                f"Fontes: {', '.join(feedback['fontes'])}"
            ])

            # Um novo feedback ainda não foi salvo
            st.session_state["feedback_salvo_texto"] = None

            st.success("Feedback gerado com sucesso!")


    # Exibe e valida o feedback gerado
    if "feedback_gerado" in st.session_state:

        st.markdown("### Revisão do feedback")

        texto_feedback = st.text_area(
            "Revise e edite o feedback antes de aprovar:",
            key="feedback_editavel",
            height=400
        )


        # Validação 1: verifica se os números existem na ficha
        resultado_numeros = validar_numeros(
            texto_feedback,
            ficha
        )


        # Validação 2: verifica se os valores correspondem
        # aos indicadores citados
        resultado_associacoes = validar_associacoes(
            texto_feedback,
            ficha
        )


        # Validação 3: verifica se os números possuem referências
        resultado_referencias = validar_referencias_completas(
            texto_feedback
        )


        st.divider()

        st.subheader("Verificação de confiabilidade")


        # As três validações precisam ser aprovadas
        if (
            resultado_numeros["valido"]
            and resultado_associacoes["valido"]
            and resultado_referencias["valido"]
        ):

            st.success(
                "Todas as verificações foram aprovadas!"
            )

            # Verifica se esse mesmo texto já foi salvo
            feedback_ja_salvo = (
                st.session_state.get("feedback_salvo_texto")
                == texto_feedback
            )

            if feedback_ja_salvo:

                st.info("Este feedback já foi salvo.")

            else:

                # Aprovação e gravação no CSV
                if st.button("Aprovar e salvar feedback"):

                    caminho = salvar_feedback_aprovado(
                        ficha,
                        texto_feedback
                    )

                    st.session_state["feedback_salvo_texto"] = texto_feedback

                    st.success(
                        "Feedback aprovado e salvo com sucesso!"
                    )

                    st.write(f"Arquivo atualizado: {caminho}")


        else:

            st.error(
                "O feedback apresenta problemas e não pode ser aprovado."
            )


            if not resultado_numeros["valido"]:

                st.write("**Números não encontrados na ficha:**")

                st.write(
                    resultado_numeros["numeros_nao_encontrados"]
                )


            if not resultado_associacoes["valido"]:

                st.write("**Problemas nas referências dos indicadores:**")

                for erro in resultado_associacoes["erros"]:

                    st.write(f"- Referência: {erro['referencia']}")

                    st.write(
                        f"  Valor informado: {erro['valor_informado']}"
                    )

                    st.write(
                        f"  Motivo: {erro['motivo']}"
                    )


            if not resultado_referencias["valido"]:

                st.write("**Números sem referência:**")

                st.write(
                    resultado_referencias["numeros_sem_referencia"]
                )


except Exception as erro:

    st.error(f"Erro ao gerar ficha ou feedback: {erro}")
