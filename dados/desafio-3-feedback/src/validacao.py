
import re


def converter_numero(texto):
    """Converte números escritos no padrão brasileiro para float."""

    texto = texto.replace("R$", "").replace("%", "").strip()

    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")

    return float(texto)


def extrair_numeros(texto):
    import re

    # Remove referências numéricas como [1], [2], [3]
    texto = re.sub(r"\[\s*\d+\s*\]", "", texto)

    # Remove datas
    texto = re.sub(
        r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}(?:-\d{2})?\b",
        "",
        texto
    )

    # Remove anos isolados
    texto = re.sub(r"\b(?:19|20)\d{2}\b", "", texto)

    # Extrai números com separadores decimais e de milhar
    encontrados = re.findall(
        r"(?<![\w])(?:R\$\s*)?-?\d+(?:\.\d{3})*(?:,\d+)?%?",
        texto
    )

    numeros = []

    for valor in encontrados:

        valor = valor.replace("R$", "").strip()
        valor = valor.replace("%", "")

        # Converte formato brasileiro para formato numérico
        valor = valor.replace(".", "").replace(",", ".")

        try:
            numeros.append(float(valor))
        except ValueError:
            continue

    return numeros
  

def coletar_numeros_ficha(ficha):
    """Reúne todos os números disponíveis na ficha de contexto."""

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

            # Conversão adicional para indicadores percentuais.
            if chave in ["conversao", "atingimento"]:
                numeros.append(float(valor) * 100)

        elif isinstance(valor, str):
            numeros.extend(extrair_numeros(valor))

    percorrer(ficha)

    return numeros


def validar_numeros(texto, ficha, tolerancia=0.02):
    """
    Verifica se todos os números do feedback estão presentes
    na ficha de contexto, permitindo pequenas diferenças
    de arredondamento.
    """

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
    import re

    # Procura referências no formato:
    # [indicadores_mes.atingimento: 164,86%]
    padrao = (
        r"\[([a-zA-Z_][\w.]*)\s*:\s*"
        r"(?:R\$\s*)?(-?\d[\d.,]*)\s*(%)?\]"
    )

    referencias = re.findall(padrao, texto)

    erros = []

    # Indicadores armazenados como proporção na ficha
    indicadores_percentuais = {
        "conversao",
        "atingimento"
    }

    for caminho, valor_texto, percentual in referencias:

        # Percorre o caminho, por exemplo:
        # indicadores_mes -> atingimento
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

        # Converte o valor escrito para número
        numeros = extrair_numeros(valor_texto)

        if not numeros:
            erros.append({
                "referencia": caminho,
                "valor_informado": valor_texto,
                "motivo": "Não foi possível interpretar o valor."
            })
            continue

        valor_informado = numeros[0]

        # A ficha guarda conversão e atingimento
        # como proporções. O texto apresenta percentuais.
        nome_indicador = partes[-1]

        if (
            percentual
            and nome_indicador in indicadores_percentuais
        ):
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
    """
    Verifica se os números apresentados no feedback
    estão acompanhados de referências aos indicadores.
    """

    import re

    # Identifica referências completas, como:
    # [indicadores_mes.conversao: 35,58%]
    # [indicadores_mes.valor_vendido: R$ 67.234,70]

    padrao_referencia = (
        r"\[[a-zA-Z_][\w.]*\s*:\s*"
        r"(?:R\$\s*)?-?\d+(?:\.\d{3})*(?:,\d+)?%?\]"
    )

    # Remove as referências completas do texto
    texto_sem_referencias = re.sub(
        padrao_referencia,
        "",
        texto
    )

    # Procura números que sobraram sem referência
    numeros_sem_referencia = extrair_numeros(
        texto_sem_referencias
    )

    return {
        "valido": len(numeros_sem_referencia) == 0,
        "numeros_sem_referencia": numeros_sem_referencia
    }
