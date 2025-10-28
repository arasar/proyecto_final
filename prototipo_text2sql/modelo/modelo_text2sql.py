def generar_sql_desde_texto(consulta_usuario, contexto):
    """
    Recibe el texto en lenguaje natural y el contexto de la base.
    Devuelve una consulta SQL generada por el modelo.
    """
    if "empleados" in consulta_usuario.lower():
        return "SELECT * FROM empleados;"
    elif "departamentos" in consulta_usuario.lower():
        return "SELECT * FROM departamentos;"
    else:
        return "-- No se pudo generar una consulta SQL válida."
