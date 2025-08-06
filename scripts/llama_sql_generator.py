# Script para usar el modelo SQL entrenado
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

class LlamaSQLGenerator:
    def __init__(self, model_path="../models/llama-sql-lora/final"):
        print("🤖 Cargando modelo SQL Llama 3.2...")
        
        # Cargar modelo base
        self.base_model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B-Instruct",
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        
        # Cargar adaptadores LoRA
        self.model = PeftModel.from_pretrained(self.base_model, model_path)
        
        # Cargar tokenizador
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        print("✅ Modelo cargado")
    
    def generar_sql(self, schema, question):
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert SQL generator. Convert natural language questions to precise SQL queries based on the provided database schema. Return only the SQL query without explanations.<|eot_id|><|start_header_id|>user<|end_header_id|>

Database Schema:
{schema}

Question: {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=800)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        if "<|start_header_id|>assistant<|end_header_id|>" in response:
            sql_part = response.split("<|start_header_id|>assistant<|end_header_id|>")[1]
            sql_part = sql_part.split("<|eot_id|>")[0].strip()
        else:
            sql_part = "Error en generación"
        
        return sql_part

# Función compatible con tu código existente
def generar_sql_con_llama(prompt):
    generator = LlamaSQLGenerator()
    # Parsear prompt simple
    if "Schema:" in prompt and "Question:" in prompt:
        schema = prompt.split("Question:")[0].replace("Schema:", "").strip()
        question = prompt.split("Question:")[1].replace("Return only the SQL query:", "").strip()
    else:
        schema = "Unknown"
        question = prompt
    
    return generator.generar_sql(schema, question)

# Ejemplo de uso
if __name__ == "__main__":
    generator = LlamaSQLGenerator()
    sql = generator.generar_sql(
        "CREATE TABLE users (id INT, name VARCHAR(50), age INT);",
        "Get users older than 25"
    )
    print(f"SQL: {sql}")
