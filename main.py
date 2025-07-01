# PASO 1: Estructura de carpetas
# Suponé que estás en la raíz de tu proyecto, creá esta estructura:

# /text2sql_project/
# ├── prompts/             # Para guardar tus prompts en archivos .txt
# ├── outputs/             # Para guardar las respuestas generadas por el modelo
# ├── scripts/             # Para tus scripts de Python
# └── main.py             # Script principal del proyecto

# # PASO 2: main.py - comenzar a cargar el dataset
# from datasets import load_dataset
# import pandas as pd

# # Cargar solo 500 ejemplos del dataset de Hugging Face
# dataset = load_dataset("gretelai/synthetic_text_to_sql", split="train[:500]")

# # Convertir a DataFrame para visualizar o procesar con mayor comodidad
# df = pd.DataFrame(dataset)

# print(df.head())

# # Guardar una copia en outputs/ para inspección manual
# df.to_csv("outputs/preview_dataset.csv", index=False)

# # PASO 3: Instalación de Ollama
# # Ejecutar desde terminal (NO desde Python):
# # 1. Descargar e instalar desde https://ollama.com/download
# # 2. Una vez instalado, en terminal:
# #    ollama pull llama3
# # 3. Para probar:
# #    ollama run llama3


# # PASO 5: Ejecutar generación en main.py (primer test)

# # Tomar una pregunta de prueba del dataset
# entrada = df.iloc[0]["sql_prompt"]
# prompt = f"Translate the following question to SQL:\n\nQuestion: {entrada}\n\nSQL:"

# # Usar el generador (verificar que Ollama esté corriendo)
# from scripts.generate_sql import generar_sql_con_ollama

# sql_generado = generar_sql_con_ollama(prompt)

# print("Pregunta:", entrada)
# print("SQL Generado:", sql_generado)

# # Guardar resultado
# test_output_path = "outputs/test_result.txt"
# with open(test_output_path, "w") as f:
#     f.write(f"Question: {entrada}\n\nSQL: {sql_generado}\n")

# main.py: carga del dataset, vista preliminar y prueba de 1 ejemplo
from datasets import load_dataset
import pandas as pd
from scripts.generate_sql import generar_sql_con_ollama

# Cargar 100 ejemplos del dataset completo
dataset = load_dataset("gretelai/synthetic_text_to_sql", split="train[:100]")
df = pd.DataFrame(dataset)

# Vista preliminar de columnas relevantes
print(df[['sql_prompt', 'sql_context', 'sql']].head())

# Tomar un ejemplo de prueba
entrada = df.iloc[0]['sql_prompt']
contexto = df.iloc[0]['sql_context']

prompt = f"""
Translate the following question to SQL based on the context provided.

Context:
{contexto}

Question:
{entrada}

SQL:
"""

sql_generado = generar_sql_con_ollama(prompt)

print("Pregunta:", entrada)
print("SQL real:", df.iloc[0]['sql'])
print("SQL generado:", sql_generado)

# Guardar en outputs
with open("outputs/test_result.txt", "w") as f:
    f.write(f"Prompt usado:\n{prompt}\n\nSQL generado:\n{sql_generado}\n")
