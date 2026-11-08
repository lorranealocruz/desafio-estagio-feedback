from src.ficha import gerar_ficha
from src.validacao import validar_associacoes

ficha = gerar_ficha("C0035", "2026-10")

# Teste 1: valores associados aos indicadores corretos
texto_correto = """
Atingimento: 164,86% [indicadores_mes.atingimento: 164,86%]

Faturamento: R$ 67.234,70
[indicadores_mes.valor_vendido: R$ 67.234,70]

Ticket médio: R$ 454,29
[indicadores_mes.ticket_medio: R$ 454,29]
"""

print("--- Teste com associações corretas ---")
print(validar_associacoes(texto_correto, ficha))


# Teste 2: valores trocados entre indicadores
texto_incorreto = """
Faturamento: R$ 454,29
[indicadores_mes.valor_vendido: R$ 454,29]

Ticket médio: R$ 67.234,70
[indicadores_mes.ticket_medio: R$ 67.234,70]
"""

print("\n--- Teste com associações incorretas ---")
print(validar_associacoes(texto_incorreto, ficha))
