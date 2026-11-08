
import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv


# Localiza a pasta principal do projeto
PASTA_DADOS = Path(__file__).resolve().parent.parent

# Carrega as variáveis do arquivo .env
load_dotenv(PASTA_DADOS / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

MODELO = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)

URL_API = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODELO}:generateContent"
)


def gerar_feedback(ficha):
    """
    Envia a ficha de contexto ao Gemini
    e retorna o feedback produzido pela IA.
    """

    if not API_KEY:
        raise ValueError(
            "Chave GEMINI_API_KEY não encontrada no .env."
        )

    instrucoes = """
    Você é um assistente especializado em feedback profissional
    para equipes de vendas do varejo.

    Sua tarefa é elaborar um feedback individual, respeitoso,
    objetivo e construtivo com base exclusivamente na ficha recebida.

    REGRAS OBRIGATÓRIAS:

    1. Utilize somente informações presentes na ficha.
    2. Não invente números, fatos, causas ou acontecimentos.
    3. Compare o vendedor com seu próprio mês anterior e com
       os indicadores gerais da loja.
    4. Nunca compare o vendedor com outros vendedores.
    5. Considere os alertas de contexto antes de interpretar
       os resultados.
    6. Não transforme questões pessoais ou de saúde em cobranças.
    7. Escolha apenas um ponto principal de melhoria.
    8. Apresente uma ação prática que possa ser realizada
       durante a próxima semana.
    9. Todo número mencionado deve conter sua fonte entre colchetes.
    10. O feedback deve ter no máximo 180 palavras.

    Retorne exclusivamente um objeto JSON válido, com as seguintes
    chaves:

    {
        "cuidados": "",
        "abertura": "",
        "ponto_forte": "",
        "ponto_a_melhorar": "",
        "pergunta_aberta": "",
        "combinado_para_a_semana": "",
        "acompanhamento": "",
        "fontes": []
    }

    Não inclua informações fora desse formato.
    """

    dados_ficha = json.dumps(
        ficha,
        ensure_ascii=False,
        indent=2
    )

    payload = {
        "systemInstruction": {
            "parts": [
                {"text": instrucoes}
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Elabore o feedback com base nesta ficha:\n"
                            + dados_ficha
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    try:
        resposta = requests.post(
            URL_API,
            headers=headers,
            json=payload,
            timeout=60
        )

        resposta.raise_for_status()

        resultado = resposta.json()

        conteudo = (
            resultado["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        feedback = json.loads(conteudo)

        return feedback

    except requests.exceptions.HTTPError as erro:
        detalhe = resposta.text[:1000]

        raise RuntimeError(
            f"Erro HTTP na API do Gemini: {erro}\n"
            f"Detalhes: {detalhe}"
        ) from erro

    except requests.exceptions.RequestException as erro:
        raise RuntimeError(
            f"Erro na comunicação com o Gemini: {erro}"
        ) from erro

    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as erro:
        raise RuntimeError(
            "A resposta do Gemini não veio no formato esperado."
        ) from erro
