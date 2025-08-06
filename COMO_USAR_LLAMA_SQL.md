# CÓMO USAR TU MODELO LLAMA SQL

## En tu run_batch.py:
```python
# Cambiar:
from scripts.generate_sql import generar_sql_con_ollama
# Por:
from scripts.llama_sql_generator import generar_sql_con_llama

# Y usar:
sql_generado = generar_sql_con_llama(prompt)
```

## Uso directo:
```python
from scripts.llama_sql_generator import LlamaSQLGenerator

generator = LlamaSQLGenerator()
sql = generator.generar_sql(schema, question)
```

## Modelo guardado en: ../models/llama-sql-lora/final
