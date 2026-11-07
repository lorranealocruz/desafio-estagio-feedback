
from src.indicadores import calcular_indicadores

# Executa os cálculos
vendedores, loja = calcular_indicadores()

print("\n===== INDICADORES DOS VENDEDORES =====")

print(
    vendedores[
        [
            "mes",
            "nome",
            "valor_vendido",
            "ticket_medio",
            "pa",
            "conversao",
            "atingimento"
        ]
    ].round(2)
)

print("\n===== INDICADORES DA LOJA =====")

print(
    loja[
        [
            "mes",
            "valor_vendido",
            "ticket_medio",
            "pa",
            "conversao",
            "atingimento"
        ]
    ].round(2)
)

# Conferência da Bianca em outubro
bianca = vendedores[
    (vendedores["nome"] == "Bianca Rocha")
    & (vendedores["mes"] == "2026-10")
].iloc[0]

print("\n===== TESTE DA BIANCA =====")
print(f"Ticket médio: R$ {bianca['ticket_medio']:.2f}")
print(f"P.A.: {bianca['pa']:.2f}")
print(f"Conversão: {bianca['conversao']:.2%}")
print(f"Atingimento: {bianca['atingimento']:.2%}")

# Testes de referência
assert round(bianca["ticket_medio"], 2) == 228.14
assert round(bianca["pa"], 2) == 1.26
assert round(bianca["conversao"] * 100) == 51
assert round(bianca["atingimento"] * 100) == 112

print("\nTodos os testes passaram!")
