# PASO 4: Crear script para usar Ollama desde Python
# Guardar este archivo como scripts/generate_sql.py

import requests
import json

def generar_sql_con_ollama(prompt: str, model: str = "llama3") -> str:
    """
    Genera SQL usando la API REST de Ollama
    """
    prompt_mejorado = f"""{prompt}

    IMPORTANT: Return ONLY the SQL query without any explanation, comments, or formatting. Do not include ```sql``` blocks."""

    try:
        url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt_mejorado,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Más determinístico para SQL
                "top_p": 0.9,
                "num_predict": 500,
            }
        }
        
        print(f"Enviando solicitud a Ollama...")
        response = requests.post(url, json=payload, timeout=200)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Error: Respuesta vacía")
        else:
            return f"Error HTTP {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "Error: No se puede conectar a Ollama. ¿Está ejecutándose 'ollama serve'?"

    except requests.exceptions.Timeout:
        return "Error: Timeout - Ollama tardó más de 60 segundos"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def test_connection():
    """
    Prueba la conexión con Ollama
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("Conexión exitosa. Modelos disponibles:")
            for model in models.get("models", []):
                print(f"- {model.get('name')}")
            return True
        else:
            print(f"Error al conectar: {response.status_code}")
            return False
    except Exception as e:
        print(f"No se puede conectar a Ollama: {e}")
        return False
