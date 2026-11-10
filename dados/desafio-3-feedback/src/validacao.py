
import re


# Reconhece referências como:
# [indicadores_mes.conversao: 47,08%]
# [indicadores_mes.conversao: 47.08%]
# [indicadores_mes.valor_vendido: R$ 32.697,48]
PADRAO_REFERENCIA = re.compile(
    r"\[([a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)\s*:\s*"
    r"(?:R\$\s*)?(-?\d[\d.,]*)(\s*%)?\]"
)


def converter_numero(texto):
    """Converte números com separadores brasileiros ou internacionais."""

    texto = texto.replace("R$", "").replace("%", "").strip()

    if "," in texto and "." in texto:
        # O último separador é considerado o separador decimal.
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")

    elif "," in texto:
        texto = texto.replace(",", ".")

    return float(texto)


def extrair_numeros(texto):
    """Extrai números de textos, aceitando ponto ou vírgula decimal."""

    texto = re.sub(r"\[\s*\d+\s*\]", "", texto)

    # Remove datas nos formatos dd/mm/aaaa e aaaa-mm ou aaaa-mm-dd.
    texto = re.sub(
        r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}(?:-\d{2})?\b",
        "",
        texto
    )

    # Remove anos isolados.
    texto = re.sub(r"\b(?:19|20)\d{2}\b", "", texto)

    encontrados = re.findall(
        r"(?<![\w])(?:R\$\s*)?-?\d+(?:[.,]\d+)*%?",
        texto
    )

    numeros = []

    for valor in encontrados:
        try:
            numeros.append(converter_numero(valor))
        except ValueError:
            continue

    return numeros


def coletar_numeros_ficha(ficha):
    """Reúne os números disponíveis na ficha de contexto."""

    numeros = []

    def percorrer(valor, chave=None):

        if isinstance(valor, dict):
            for nome, conteudo in valor.items():
                percorrer(conteudo, nome)

        elif isinstance(valor, list):
            for item in valor:
                percorrer(item)

        elif isinstance(valor, (int, float)) and not isinstance(valor, bool):
            numeros.append(float(valor))

            # Conversão adicional dos indicadores armazenados como proporção.
            if chave in ["conversao", "atingimento"]:
                numeros.append(float(valor) * 100)

        elif isinstance(valor, str):
            numeros.extend(extrair_numeros(valor))

    percorrer(ficha)

    return numeros


def validar_numeros(texto, ficha, tolerancia=0.02):
    """Verifica se os números do feedback existem na ficha."""

    numeros_texto = extrair_numeros(texto)
    numeros_ficha = coletar_numeros_ficha(ficha)

    nao_encontrados = []

    for numero in numeros_texto:

        encontrado = any(
            abs(numero - referencia) <= tolerancia
            for referencia in numeros_ficha
        )

        if not encontrado and numero not in nao_encontrados:
            nao_encontrados.append(numero)

    return {
        "valido": len(nao_encontrados) == 0,
        "numeros_nao_encontrados": nao_encontrados
    }


def validar_associacoes(texto, ficha, tolerancia=0.02):
    """Verifica se cada referência corresponde ao indicador informado."""

    referencias = PADRAO_REFERENCIA.findall(texto)

    erros = []

    indicadores_percentuais = {
        "conversao",
        "atingimento"
    }

    for caminho, valor_texto, percentual in referencias:

        partes = caminho.split(".")
        valor_ficha = ficha

        try:
            for parte in partes:
                valor_ficha = valor_ficha[parte]

            valor_ficha = float(valor_ficha)

        except (KeyError, TypeError, ValueError):
            erros.append({
                "referencia": caminho,
                "valor_informado": valor_texto,
                "motivo": "Fonte não encontrada na ficha."
            })
            continue

        try:
            valor_informado = converter_numero(valor_texto)

        except ValueError:
            erros.append({
                "referencia": caminho,
                "valor_informado": valor_texto,
                "motivo": "Não foi possível interpretar o valor."
            })
            continue

        nome_indicador = partes[-1]

        if percentual and nome_indicador in indicadores_percentuais:
            valor_ficha *= 100

        if abs(valor_informado - valor_ficha) > tolerancia:
            erros.append({
                "referencia": caminho,
                "valor_informado": valor_informado,
                "valor_correto": valor_ficha,
                "motivo": "O valor não corresponde ao indicador."
            })

    return {
        "valido": len(referencias) > 0 and len(erros) == 0,
        "total_referencias": len(referencias),
        "erros": erros
    }


def validar_referencias_completas(texto):
    """Verifica se os números estão acompanhados de referências."""

    referencias = list(PADRAO_REFERENCIA.finditer(texto))

    partes = []
    inicio = 0

    for referencia in referencias:

        # Trecho entre a referência anterior e a referência atual.
        trecho = texto[inicio:referencia.start()]

        valor_referencia = converter_numero(referencia.group(2))

        padrao_numero = r"(?<![\w])(?:R\$\s*)?-?\d+(?:[.,]\d+)*%?"

        numeros_trecho = list(re.finditer(padrao_numero, trecho))

        # Procura, de trás para frente, o número correspondente
        # ao valor informado na referência.
        for numero in reversed(numeros_trecho):

            try:
                valor_texto = converter_numero(numero.group())

                if abs(valor_texto - valor_referencia) <= 0.00001:

                    trecho = (
                        trecho[:numero.start()]
                        + trecho[numero.end():]
                    )

                    break

            except ValueError:
                continue

        partes.append(trecho)

        inicio = referencia.end()

    # Acrescenta o restante do texto após a última referência.
    partes.append(texto[inicio:])

    texto_sem_referencias = "".join(partes)

    numeros_sem_referencia = extrair_numeros(texto_sem_referencias)

    return {
        "valido": len(numeros_sem_referencia) == 0,
        "numeros_sem_referencia": numeros_sem_referencia
    }




def validar_estrutura_feedback(feedback):
    """Verifica se a resposta da IA contém todos os campos obrigatórios."""

    campos_obrigatorios = [
        "cuidados",
        "abertura",
        "ponto_forte",
        "ponto_a_melhorar",
        "pergunta_aberta",
        "combinado_para_a_semana",
        "acompanhamento",
        "fontes"
    ]

    erros = []

    for campo in campos_obrigatorios:

        if campo not in feedback:
            erros.append(f"Campo ausente: {campo}")
            continue

        valor = feedback[campo]

        if campo == "fontes":

            if not isinstance(valor, list) or not valor:
                erros.append("O campo fontes deve ser uma lista preenchida.")

        elif not isinstance(valor, str) or not valor.strip():
            erros.append(f"O campo {campo} está vazio ou inválido.")

    return {
        "valido": len(erros) == 0,
        "erros": erros
    }


def validar_qualidade_feedback(texto):
    """Verifica aspectos básicos de organização e apresentação."""

    secoes_obrigatorias = [
        "Cuidados:",
        "Abertura:",
        "Ponto forte:",
        "Ponto a melhorar:",
        "Pergunta aberta:",
        "Combinado para a semana:",
        "Acompanhamento:",
        "Fontes:"
    ]

    erros = []
    secoes_encontradas = {}

    for secao in secoes_obrigatorias:

        padrao = (
            re.escape(secao)
            + r"\s*(.*?)(?=\n\s*\n[A-ZÁÉÍÓÚÂÊÔÃÕÇ][^:\n]*:|$)"
        )

        resultado = re.search(
            padrao,
            texto,
            flags=re.DOTALL
        )

        if not resultado:
            erros.append(f"Seção ausente: {secao}")
            continue

        conteudo = resultado.group(1).strip()

        if not conteudo:
            erros.append(f"Seção vazia: {secao}")
        else:
            secoes_encontradas[secao] = conteudo

    if re.search(r"!{2,}", texto):
        erros.append("Excesso de pontos de exclamação.")

    if re.search(r"\?{2,}", texto):
        erros.append("Excesso de pontos de interrogação.")

    for secao, conteudo in secoes_encontradas.items():

        if len(conteudo) > 600:
            erros.append(
                f"A seção {secao} está muito extensa."
            )

    return {
        "valido": len(erros) == 0,
        "erros": erros
    }
