
from src.contexto import gerar_alertas


# Cenários que precisamos validar
casos = [
    {
        "nome": "Renata - Setembro",
        "vendedor_id": "C0036",
        "mes": "2026-09",
        "esperado": ["férias", "8 dias"]
    },
    {
        "nome": "Lucas - Setembro",
        "vendedor_id": "C0034",
        "mes": "2026-09",
        "esperado": ["90 dias"]
    },
    {
        "nome": "Lucas - Outubro",
        "vendedor_id": "C0034",
        "mes": "2026-10",
        "esperado": ["90 dias"]
    },
    {
        "nome": "Vanessa - Outubro",
        "vendedor_id": "C0038",
        "mes": "2026-10",
        "esperado": ["5x2"]
    },
    {
        "nome": "Marcelo - Outubro",
        "vendedor_id": "C0035",
        "mes": "2026-10",
        "esperado": ["sensível"]
    }
]


for caso in casos:
    alertas = gerar_alertas(
        caso["vendedor_id"],
        caso["mes"]
    )

    texto_alertas = " ".join(alertas).lower()

    print(f"\n--- {caso['nome']} ---")

    if alertas:
        for alerta in alertas:
            print(f"- {alerta}")
    else:
        print("Nenhum alerta identificado.")

    # Confere se os alertas esperados apareceram
    for palavra in caso["esperado"]:
        assert palavra.lower() in texto_alertas, (
            f"ERRO: '{palavra}' não foi encontrado em {caso['nome']}."
        )

    print("Teste das condições esperadas: OK")


print("\nTodos os cenários foram validados!")
