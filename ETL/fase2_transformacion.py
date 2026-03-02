def transformar_datos(datos_crudos):
    """Fase 2: Transforma y simplifica la estructura original."""
    # Marca el inicio de la fase de transformación.
    print("=== INICIO FASE 2: TRANSFORMACIÓN ===")

    # Aquí guardaremos los países ya adaptados al formato final.
    datos_transformados = []

    # Recorremos cada país del JSON original de la API.
    for pais in datos_crudos:
        # Extrae el nombre común del país.
        # Si no existe, usa "Sin nombre" para evitar errores.
        nombre = pais.get("name", {}).get("common", "Sin nombre")

        # "capital" puede venir como lista o no existir.
        # Tomamos la primera capital disponible.
        capital_lista = pais.get("capital", [])
        capital = capital_lista[0] if capital_lista else "Sin capital"

        # Extraemos campos numéricos y de clasificación con valores por defecto.
        region = pais.get("region", "Sin región")
        poblacion = pais.get("population", 0)
        area = pais.get("area", 0)

        # Construimos un registro simple y uniforme para análisis.
        registro_simplificado = {
            "nombre": nombre,
            "capital": capital,
            "region": region,
            "poblacion": poblacion,
            "area": area,
        }

        # Agregamos el registro transformado a la lista final.
        datos_transformados.append(registro_simplificado)

    # Resumen del total transformado.
    print(f"Transformación completada: {len(datos_transformados)} registros simplificados.")
    print("=== FIN FASE 2: TRANSFORMACIÓN ===\n")

    # Retorna datos listos para almacenarse.
    return datos_transformados
