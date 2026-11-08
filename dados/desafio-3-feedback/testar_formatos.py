from src.validacao import extrair_numeros

texto = """
Meta: R$ 40.782,86
Atingimento: 164,86%
Vendas: R$ 67.234,70
Ticket médio: R$ 454,29
Número inventado: 999,99
Data: 03/10/2026
"""

print(extrair_numeros(texto))