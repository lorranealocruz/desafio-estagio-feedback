
from src.ficha import gerar_ficha
from src.validacao import validar_numeros


ficha = gerar_ficha("C0035", "2026-10")


# Teste 1: números existentes na ficha
feedback_correto = """
Em outubro, Marcelo vendeu R$ 67.234,70.
Seu ticket médio foi de R$ 454,29.
A conversão foi de 35,58%.
O atingimento da meta foi de 164,86%.
"""


resultado_correto = validar_numeros(
    feedback_correto,
    ficha
)

print("--- Teste com números corretos ---")
print(resultado_correto)


# Teste 2: número inventado
feedback_incorreto = """
Em outubro, Marcelo vendeu R$ 67.234,70.
Seu ticket médio foi de R$ 454,29.
Ele faturou R$ 99.999,00.
"""


resultado_incorreto = validar_numeros(
    feedback_incorreto,
    ficha
)

print("\n--- Teste com número inventado ---")
print(resultado_incorreto)
