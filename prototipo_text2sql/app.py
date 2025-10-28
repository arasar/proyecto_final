import streamlit as st
from utils.db_utils import obtener_contexto_tablas, ejecutar_consulta
from modelo.modelo_text2sql import generar_sql_desde_texto

DB_PATH = "empresa.db"

st.set_page_config(page_title="Prototipo Text-to-SQL", layout="centered")

st.title("🧠 Prototipo Text-to-SQL")
st.write("Ingresá una consulta en lenguaje natural para obtener su equivalente en SQL.")

consulta_usuario = st.text_area("Consulta en lenguaje natural", height=100)
btn_traducir = st.button("🔍 Traducir a SQL")

if btn_traducir and consulta_usuario.strip():
    with st.spinner("Generando consulta SQL..."):
        contexto = obtener_contexto_tablas(DB_PATH)
        prompt = f"Contexto:\n{contexto}\n\nConsulta:\n{consulta_usuario}"
        st.subheader("🧾 Prompt generado")
        st.code(prompt, language="markdown")

        sql_generada = generar_sql_desde_texto(consulta_usuario, contexto)

        st.subheader("💬 Consulta SQL generada")
        st.code(sql_generada, language="sql")

        if sql_generada.strip().lower().startswith("select"):
            st.subheader("📊 Resultados de la consulta")
            resultados = ejecutar_consulta(DB_PATH, sql_generada)
            st.dataframe(resultados, use_container_width=True)
        else:
            st.info("La consulta no es de tipo SELECT, por lo tanto no se ejecuta en la base.")
