import json


def cargar_datos(datos_transformados, archivo_salida):
    """Fase 3: Carga los datos transformados en un archivo JSON local."""
    print("=== INICIO FASE 3: CARGA ===")

    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        json.dump(datos_transformados, archivo, ensure_ascii=False, indent=4)

    print(f"Carga completada: datos guardados en '{archivo_salida}'.")
    print("=== FIN FASE 3: CARGA ===")
