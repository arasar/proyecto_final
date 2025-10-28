import sqlite3
import pandas as pd

def obtener_contexto_tablas(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    

        contexto = ""
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        for (tabla,) in tablas:
            cursor.execute(f"PRAGMA table_info({tabla});")
            columnas = cursor.fetchall()
            columnas_str = ", ".join([col[1] for col in columnas])
            contexto += f"Tabla: {tabla} (Columnas: {columnas_str})\n"

        conn.close()
    except sqlite3.Error as e:
        contexto = f"Error al obtener el contexto de la base de datos: {e}"
    return contexto

def ejecutar_consulta(db_path, query):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        df = pd.DataFrame({"Error": [str(e)]})
    conn.close()
    return df