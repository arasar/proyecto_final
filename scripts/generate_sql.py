# PASO 4: Crear script para usar Ollama desde Python
# Guardar este archivo como scripts/generate_sql.py

import subprocess
import json

def generar_sql_con_ollama(prompt: str) -> str:
    """
    Ejecuta el modelo llama3 localmente con Ollama para generar SQL a partir de un prompt.
    """
    comando = [
        "ollama", "run", "llama3",
        "--prompt", prompt
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.stdout.strip()