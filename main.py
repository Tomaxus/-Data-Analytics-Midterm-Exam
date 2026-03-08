from ETL.fase3_carga import cargar_datos
from ETL.fase1_extraccion import extraer_datos
from ETL.fase2_transformacion import transformar_datos


def main():
    url_api = "https://restcountries.com/v3.1/all"

    archivo_salida = "paises_transformados.json"

    datos_crudos = extraer_datos(url_api)
    datos_transformados = transformar_datos(datos_crudos)
    cargar_datos(datos_transformados, archivo_salida)


if __name__ == "__main__":
    main()
