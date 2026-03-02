import json


def cargar_datos(datos_transformados, archivo_salida):
    """Fase 3: Carga los datos transformados en un archivo JSON local."""
    # Mensaje de control de inicio de la fase de carga.
    print("=== INICIO FASE 3: CARGA ===")

    # Abre (o crea) el archivo de salida en modo escritura con codificación UTF-8.
    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        # Guarda la lista de países transformados en formato JSON legible.
        # ensure_ascii=False conserva tildes/ñ correctamente.
        # indent=4 mejora la lectura del archivo generado.
        json.dump(datos_transformados, archivo, ensure_ascii=False, indent=4)

    # Confirmación de ruta de salida.
    print(f"Carga completada: datos guardados en '{archivo_salida}'.")
    print("=== FIN FASE 3: CARGA ===")
