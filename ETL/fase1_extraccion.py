import requests


def extraer_datos(url):
    """Fase 1: Extrae datos crudos desde la API de REST Countries."""
    print("=== INICIO FASE 1: EXTRACCIÓN ===")

    try:
        respuesta = requests.get(url, timeout=30)

        if respuesta.status_code == 400 and "fields" in respuesta.text.lower():
            print("El endpoint general devolvió 400; se aplica fallback con fields mínimos.")
            url_fallback = f"{url}?fields=name,capital,region,population,area"
            respuesta = requests.get(url_fallback, timeout=30)

        respuesta.raise_for_status()

        datos_crudos = respuesta.json()

        print(f"Extracción completada: {len(datos_crudos)} registros obtenidos.")
        print("=== FIN FASE 1: EXTRACCIÓN ===\n")

        return datos_crudos
    except requests.exceptions.RequestException as error:
        print(f"Error durante la extracción: {error}")
        raise
