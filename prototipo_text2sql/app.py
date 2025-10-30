import streamlit as st
from utils.db_utils import obtener_contexto_tablas, ejecutar_consulta
from modelo.modelo_text2sql import generar_sql_desde_texto

DB_PATH = "prototipo_text2sql\data\chinook.db"

st.set_page_config(page_title="Prototipo Text-to-SQL", layout="wide")

st.title("🧠 Prototipo Text-to-SQL")

# Layout en dos columnas
col1, col2 = st.columns([1, 1], gap="large")

# Columna izquierda: entrada y prompt generado
with col1:
    st.write("Ingresá una consulta en lenguaje natural para obtener su equivalente en SQL.")
    consulta_usuario = st.text_area("Consulta en lenguaje natural", height=140)
    btn_traducir = st.button("🔍 Traducir a SQL")

    # Mostrar prompt generado (si ya hay texto)
    if consulta_usuario.strip() and not btn_traducir:
        contexto_preview = obtener_contexto_tablas(DB_PATH)
        prompt_preview = f"Contexto:\n{contexto_preview}\n\nConsulta:\n{consulta_usuario}"
        st.subheader("🧾 Prompt (previsualización)")
        st.code(prompt_preview, language="markdown")

# Columna derecha: resultado y ejecución
with col2:
    # Crear placeholders (contenedores) en el orden que se quiere mostrar: primero SQL, luego resultados
    placeholder_sql = st.empty()
    placeholder_results = st.empty()

# Si se pulsa traducir, generar y mostrar en la columna derecha (y prompt final en la izquierda)
if btn_traducir and consulta_usuario.strip():
    with st.spinner("Generando consulta SQL..."):
        contexto = obtener_contexto_tablas(DB_PATH)
        prompt = f"Contexto:\n{contexto}\n\nConsulta:\n{consulta_usuario}"

        # Mostrar prompt generado en la columna izquierda
        with col1:
            st.subheader("🧾 Prompt generado")
            st.code(prompt, language="markdown")

        # Generar SQL con el modelo
        sql_generada = generar_sql_desde_texto(consulta_usuario, contexto)

        # Usar los containers para mantener título + contenido sin sobrescribir
        with col2:
            sql_container = placeholder_sql.container()
            sql_container.subheader("💬 Consulta SQL generada")
            sql_container.code(sql_generada, language="sql")

            results_container = placeholder_results.container()
            if sql_generada.strip().lower().startswith("select"):
                results_container.subheader("📊 Resultados de la consulta")
                try:
                    resultados = ejecutar_consulta(DB_PATH, sql_generada)
                    results_container.dataframe(resultados, use_container_width=True)
                except Exception as e:
                    results_container.error(f"Error al ejecutar la consulta: {e}")
            else:
                results_container.info("La consulta no es de tipo SELECT, por lo tanto no se ejecuta en la base.")
