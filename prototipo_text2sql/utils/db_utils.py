import sqlite3
import pandas as pd

def obtener_contexto_tablas(db_path: str) -> str:
    """
    Obtiene la estructura de todas las tablas de la base de datos
    consultando la columna 'sql' de sqlite_master, que contiene el
    comando CREATE TABLE exacto. Esto replica el formato usado en el
    entrenamiento del modelo.
    """
    conn = None
    contexto_sql = ""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Consulta CLAVE: Selecciona la columna 'sql' de sqlite_master
        sql_query = """
        SELECT sql 
        FROM sqlite_master 
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%' 
        ORDER BY name;
        """
        
        cursor.execute(sql_query)
        esquemas = cursor.fetchall()
        
        # Concatena los esquemas en una sola cadena
        for esquema in esquemas:
            # esquema[0] es la cadena 'CREATE TABLE ...'
            contexto_sql += esquema[0] + ";\n"
            
    except sqlite3.Error as e:
        contexto_sql = f"Error al obtener el contexto de las tablas: {e}"
    finally:
        if conn:
            conn.close()
            
    return contexto_sql

def ejecutar_consulta(db_path, query):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        df = pd.DataFrame({"Error": [str(e)]})
    conn.close()
    return df

def formatear_prompt_llama(schema: str, question: str) -> str:
    """
    Formatea el contexto (schema) y la pregunta (question) en el template 
    de Llama 3.1 para la inferencia (Text-to-SQL).

    Args:
        schema: La estructura de la base de datos (CREATE TABLE statements).
        question: La pregunta del usuario en lenguaje natural.

    Returns:
        La cadena de prompt completa lista para enviar al modelo LLM.
    """
    
    # 1. Definición de la Instrucción del Sistema (Rol del LLM)
    SYSTEM_INSTRUCTION = "You are an expert SQL generator. Convert natural language questions to precise SQL queries based on the provided database schema. Return only the SQL query without explanations. Always end queries with semicolon and use proper SQL formatting."
    
    # 2. Template Llama 3.1 para el prompt de inferencia
    # La salida final debe terminar en "<|start_header_id|>assistant<|end_header_id|>", 
    # esperando que el modelo genere el SQL.
    TEMPLATE_PROMPT = (
        "<|begin_of_text|>"
        "<|start_header_id|>system<|end_header_id|>\n{system_instruction}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
        "Database Schema:\n{schema}\n"
        "Question: {question}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>"
    )
    
    prompt = TEMPLATE_PROMPT.format(
        system_instruction=SYSTEM_INSTRUCTION.strip(),
        schema=schema.strip(),
        question=question.strip()
    )
    
    return prompt