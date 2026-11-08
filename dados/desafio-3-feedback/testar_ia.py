
from src.ficha import gerar_ficha
from src.ia import gerar_feedback
import json


# Seleciona Marcelo em outubro
ficha = gerar_ficha("C0035", "2026-10")

print("Enviando ficha para a inteligência artificial...\n")

try:
    feedback = gerar_feedback(ficha)

    print("Feedback recebido com sucesso!\n")

    print(json.dumps(
        feedback,
        indent=4,
        ensure_ascii=False
    ))

    # Verifica se todas as chaves esperadas existem
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

    faltantes = [
        campo
        for campo in campos_obrigatorios
        if campo not in feedback
    ]

    if faltantes:
        print("\nCampos ausentes:", faltantes)
    else:
        print("\nTodos os campos obrigatórios estão presentes!")

except Exception as erro:
    print(f"\nErro durante o teste: {erro}")
