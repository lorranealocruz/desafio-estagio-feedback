
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
    """Extrai números de um texto, ignorando datas."""

    # Remove datas como 03/10/2026 e 2026-10-03
    texto = re.sub(
        r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}(?:-\d{2})?\b",
        " ",
        texto
    )

    padrao = r"(?<![\w/])(?:R\$\s*)?-?\d+(?:[.,]\d+)*(?:\s*%)?(?![\w/])"

    encontrados = re.findall(padrao, texto)

    numeros = []

    for item in encontrados:
        try:
            numeros.append(converter_numero(item))
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
