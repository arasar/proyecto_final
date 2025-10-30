def generar_sql_desde_texto(consulta_usuario, contexto):
    """
    Recibe el texto en lenguaje natural y el contexto de la base.
    Devuelve una consulta SQL generada por el modelo.
    """
    if "employees" in consulta_usuario.lower():
        return "SELECT * FROM employees;"
    elif "customers" in consulta_usuario.lower():
        return "SELECT * FROM customers;"
    else:
        return "-- No se pudo generar una consulta SQL válida."
