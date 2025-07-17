import pandas as pd
import json
import os
from datasets import load_dataset

def preparar_datos_entrenamiento():
    """
    Prepara los datos en formato para fine-tuning
    """
    print("Cargando dataset...")
    dataset = load_dataset("gretelai/synthetic_text_to_sql", split="train[:1000]")
    df = pd.DataFrame(dataset)
    
    # Crear datos de entrenamiento en formato JSONL
    training_data = []
    
    for _, row in df.iterrows():
        # Formato para Ollama fine-tuning
        entrada = {
            "instruction": f"""Convert this question to SQL:

Schema: {row['sql_context']}
Question: {row['sql_prompt']}

Return only the SQL query:""",
            "output": row['sql']
        }
        training_data.append(entrada)
    
    return training_data

def crear_modelfile(training_data):
    """
    Crea un Modelfile para Ollama con los datos de entrenamiento
    """
    modelfile_content = f"""FROM llama3

# Datos de entrenamiento específicos para SQL
TEMPLATE \"\"\"<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert SQL generator. Convert natural language questions to SQL queries based on the provided database schema. Return only the SQL query without explanations.

<|eot_id|><|start_header_id|>user<|end_header_id|>

{{{{ .Prompt }}}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

\"\"\"

# Parámetros optimizados para SQL
PARAMETER temperature 0.1
PARAMETER top_p 0.8
PARAMETER top_k 50
PARAMETER repeat_penalty 1.15
PARAMETER num_predict 200
PARAMETER stop "<|eot_id|>"

# System message para SQL
SYSTEM "You are an expert SQL generator. Convert natural language questions to SQL queries. Return only the SQL query without explanations or formatting."
"""

    # Agregar ejemplos de entrenamiento como few-shot learning
    for i, example in enumerate(training_data[:20]):  # Solo primeros 20 ejemplos
        modelfile_content += f'\nMESSAGE user "{example["instruction"]}"\n'
        modelfile_content += f'MESSAGE assistant "{example["output"]}"\n'

    return modelfile_content

def entrenar_modelo():
    """
    Función principal de entrenamiento
    """
    print("=== INICIANDO ENTRENAMIENTO DEL MODELO SQL ===")
    
    # 1. Preparar datos
    training_data = preparar_datos_entrenamiento()
    print(f"✓ Datos preparados: {len(training_data)} ejemplos")
    
    # 2. Crear Modelfile
    modelfile = crear_modelfile(training_data)
    
    # 3. Guardar Modelfile
    os.makedirs("models", exist_ok=True)
    with open("models/Modelfile.sql", "w", encoding="utf-8") as f:
        f.write(modelfile)
    print("✓ Modelfile creado: models/Modelfile.sql")
    
    # 4. Guardar datos de entrenamiento
    with open("models/training_data.jsonl", "w", encoding="utf-8") as f:
        for example in training_data:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    print("✓ Datos de entrenamiento guardados: models/training_data.jsonl")
    
    print("\n=== PASOS PARA CREAR EL MODELO ===")
    print("1. Ejecuta en terminal:")
    print("   cd models")
    print("   ollama create sql-expert -f Modelfile.sql")
    print("\n2. Probar el modelo:")
    print("   ollama run sql-expert")
    print("\n3. En tu código, usar:")
    print("   generar_sql_con_ollama(prompt, model='sql-expert')")

if __name__ == "__main__":
    entrenar_modelo()