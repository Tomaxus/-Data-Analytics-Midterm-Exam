def transformar_datos(datos_crudos):
    """Fase 2: Transforma y simplifica la estructura original."""
    print("=== INICIO FASE 2: TRANSFORMACIÓN ===")

    datos_transformados = []

    for pais in datos_crudos:
        nombre = pais.get("name", {}).get("common", "Sin nombre")

        capital_lista = pais.get("capital", [])
        capital = capital_lista[0] if capital_lista else "Sin capital"

        region = pais.get("region", "Sin región")
        poblacion = pais.get("population", 0)
        area = pais.get("area", 0)

        registro_simplificado = {
            "nombre": nombre,
            "capital": capital,
            "region": region,
            "poblacion": poblacion,
            "area": area,
        }

        datos_transformados.append(registro_simplificado)

    print(f"Transformación completada: {len(datos_transformados)} registros simplificados.")
    print("=== FIN FASE 2: TRANSFORMACIÓN ===\n")

    return datos_transformados
