import requests

def test_ollama():
    try:
        # Probar si Ollama está ejecutándose
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Modelos: {response.json()}")
        
        # Probar una consulta muy simple
        payload = {
            "model": "llama3",
            "prompt": "Say hello",
            "stream": False
        }
        
        print("Enviando consulta simple...")
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        print(f"Respuesta: {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama()