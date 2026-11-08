
from src.ficha import gerar_ficha
import json

ficha = gerar_ficha("C0035", "2026-10")

print(json.dumps(
    ficha,
    indent=4,
    ensure_ascii=False
))
