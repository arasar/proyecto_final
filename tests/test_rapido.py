# Test rápido
from scripts.generate_sql import generar_sql_con_ollama

prompt = """Convert this question to SQL:

Schema: CREATE TABLE users (id INT, name TEXT, age INT);
Question: Get all users older than 25

Return only the SQL query:"""

resultado = generar_sql_con_ollama(prompt)
print(resultado)