import requests


def extraer_datos(url):
    """Fase 1: Extrae datos crudos desde la API de REST Countries."""
    # Mensaje de control para identificar el inicio de la fase de extracción.
    print("=== INICIO FASE 1: EXTRACCIÓN ===")

    try:
        # Se hace una petición HTTP GET al endpoint principal.
        # timeout=30 evita que el programa quede esperando indefinidamente.
        respuesta = requests.get(url, timeout=30)

        # Algunas veces la API exige especificar campos concretos y responde 400.
        # Si eso ocurre, aplicamos un fallback solicitando solo los campos necesarios.
        if respuesta.status_code == 400 and "fields" in respuesta.text.lower():
            print("El endpoint general devolvió 400; se aplica fallback con fields mínimos.")
            url_fallback = f"{url}?fields=name,capital,region,population,area"
            respuesta = requests.get(url_fallback, timeout=30)

        # Si la respuesta no es exitosa (2xx), se lanza una excepción HTTP.
        respuesta.raise_for_status()

        # Convertimos el JSON recibido (lista de países) a estructura Python.
        datos_crudos = respuesta.json()

        # Resumen de cuántos registros se extrajeron.
        print(f"Extracción completada: {len(datos_crudos)} registros obtenidos.")
        print("=== FIN FASE 1: EXTRACCIÓN ===\n")

        # La función retorna los datos crudos para la siguiente fase.
        return datos_crudos
    except requests.exceptions.RequestException as error:
        # Captura errores de red, timeout o respuestas HTTP inválidas.
        print(f"Error durante la extracción: {error}")
        # Re-lanza el error para que el flujo principal sepa que falló.
        raise
