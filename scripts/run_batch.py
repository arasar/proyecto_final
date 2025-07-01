# Nuevo script: scripts/run_batch.py
# Ejecuta múltiples ejemplos y guarda resultados en CSV
import pandas as pd
from datasets import load_dataset
from scripts.generate_sql import generar_sql_con_ollama

# Cargar 100 ejemplos del dataset completo
dataset = load_dataset("gretelai/synthetic_text_to_sql", split="train[:100]")
df = pd.DataFrame(dataset)

resultados = []

for i, row in df.iterrows():
    pregunta = row['sql_prompt']
    contexto = row['sql_context']
    sql_real = row['sql']
    dominio = row.get('domain', '')
    complejidad = row.get('sql_complexity', '')

    prompt = f"""
    Translate the following question to SQL based on the context provided.

    Context:
    {contexto}

    Question:
    {pregunta}

    SQL:
    """
    try:
        sql_generado = generar_sql_con_ollama(prompt)
    except Exception as e:
        sql_generado = f"[ERROR: {str(e)}]"

    coincide = sql_generado.strip().lower() == sql_real.strip().lower()

    resultados.append({
        "pregunta": pregunta,
        "contexto": contexto,
        "sql_real": sql_real,
        "sql_generado": sql_generado,
        "coincide": coincide,
        "dominio": dominio,
        "complejidad": complejidad
    })

resultados_df = pd.DataFrame(resultados)
resultados_df.to_csv("outputs/resultados_batch.csv", index=False)
print("✔ Resultados guardados en outputs/resultados_batch.csv")