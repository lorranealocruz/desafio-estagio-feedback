
from src.ficha import gerar_ficha
from src.registro import salvar_feedback_aprovado


# Gera a ficha do Marcelo para outubro
ficha = gerar_ficha("C0035", "2026-10")

# Cria um feedback fictício para testar o salvamento
texto_feedback = """
Ponto forte: Superou a meta do mês.
Ponto a melhorar: Melhorar a conversão.
Combinado: Acompanhar os resultados diariamente.
"""

print("Salvando feedback de teste...")

caminho = salvar_feedback_aprovado(
    ficha,
    texto_feedback,
    "saidas/teste_feedbacks.csv"
)

print("\nFeedback salvo com sucesso!")
print(f"Arquivo: {caminho}")
