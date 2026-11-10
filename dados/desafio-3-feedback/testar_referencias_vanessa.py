
from src.validacao import (
    PADRAO_REFERENCIA,
    validar_referencias_completas
)

texto = """
Você realizou 93 vendas [indicadores_mes.vendas: 93]
e obteve R$ 25.762,18
[indicadores_mes.valor_vendido: R$ 25.762,18].

Seu atingimento foi de 71,57%
[indicadores_mes.atingimento: 71,57%].
"""

print("--- Referências identificadas ---")
print(PADRAO_REFERENCIA.findall(texto))

print("\n--- Resultado da validação ---")
print(validar_referencias_completas(texto))

from src.validacao import PADRAO_REFERENCIA, extrair_numeros

texto_sem_referencias = PADRAO_REFERENCIA.sub("", texto)

print("\n--- Texto após remover as referências ---")
print(texto_sem_referencias)

print("\n--- Números restantes ---")
print(extrair_numeros(texto_sem_referencias))