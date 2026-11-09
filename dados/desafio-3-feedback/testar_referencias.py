
from src.validacao import validar_referencias_completas


# Teste 1: número com referência
texto_correto = """
Sua conversão foi de
[indicadores_mes.conversao: 35,58%].
"""

# Teste 2: número sem referência
texto_incorreto = """
Sua conversão foi de 35,58%.
"""


print("--- Teste com referência completa ---")

resultado = validar_referencias_completas(texto_correto)

print(resultado)


print("\n--- Teste sem referência ---")

resultado = validar_referencias_completas(texto_incorreto)

print(resultado)
