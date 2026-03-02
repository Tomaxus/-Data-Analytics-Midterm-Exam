from ETL.fase3_carga import cargar_datos
from ETL.fase1_extraccion import extraer_datos
from ETL.fase2_transformacion import transformar_datos


def main():
    # Endpoint de donde se obtienen todos los países.
    url_api = "https://restcountries.com/v3.1/all"

    # Nombre del archivo JSON que se generará con los datos procesados.
    archivo_salida = "paises_transformados.json"

    # Flujo ETL completo:
    # 1) extraer datos crudos desde API
    # 2) transformar al formato simplificado
    # 3) cargar (guardar) en archivo local
    datos_crudos = extraer_datos(url_api)
    datos_transformados = transformar_datos(datos_crudos)
    cargar_datos(datos_transformados, archivo_salida)


if __name__ == "__main__":
    # Ejecuta el ETL solo cuando este archivo se corre directamente.
    main()
