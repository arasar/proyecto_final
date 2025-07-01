# PASO 4: Crear script para usar Ollama desde Python
# Guardar este archivo como scripts/generate_sql.py

import subprocess

def generar_sql_con_ollama(prompt: str) -> str:
    try:
        proceso = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        out, err = proceso.communicate(input=prompt, timeout=90)

        if err:
            return f"[ERROR STDERR: {err.strip()}]"

        return out.strip()

    except subprocess.TimeoutExpired:
        return "[ERROR: El modelo tardó demasiado en responder (timeout)]"
    except Exception as e:
        return f"[ERROR inesperado: {str(e)}]"
