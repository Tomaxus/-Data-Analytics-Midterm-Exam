import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def cargar_datos(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def grafica_cantidad_paises_por_region(datos, carpeta_salida):
    conteo = Counter(pais.get("region", "Sin región") for pais in datos)
    regiones_ordenadas = sorted(conteo.items(), key=lambda item: item[1], reverse=True)

    regiones = [item[0] for item in regiones_ordenadas]
    cantidades = [item[1] for item in regiones_ordenadas]

    plt.figure(figsize=(10, 6))
    barras = plt.bar(regiones, cantidades)
    plt.title("Cantidad de países por región")
    plt.xlabel("Región")
    plt.ylabel("Número de países")
    plt.xticks(rotation=25)

    for barra, valor in zip(barras, cantidades):
        plt.text(barra.get_x() + barra.get_width() / 2, valor, str(valor), ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(carpeta_salida / "01_cantidad_paises_por_region.png", dpi=150)
    plt.close()


def grafica_poblacion_total_por_region(datos, carpeta_salida):
    poblacion_por_region = defaultdict(int)
    for pais in datos:
        region = pais.get("region", "Sin región")
        poblacion_por_region[region] += pais.get("poblacion", 0)

    regiones_ordenadas = sorted(poblacion_por_region.items(), key=lambda item: item[1], reverse=True)
    regiones = [item[0] for item in regiones_ordenadas]
    poblaciones = [item[1] for item in regiones_ordenadas]

    plt.figure(figsize=(10, 6))
    plt.bar(regiones, poblaciones)
    plt.title("Población total por región")
    plt.xlabel("Región")
    plt.ylabel("Población total")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(carpeta_salida / "02_poblacion_total_por_region.png", dpi=150)
    plt.close()


def grafica_area_total_por_region(datos, carpeta_salida):
    area_por_region = defaultdict(float)
    for pais in datos:
        region = pais.get("region", "Sin región")
        area_por_region[region] += pais.get("area", 0)

    regiones_ordenadas = sorted(area_por_region.items(), key=lambda item: item[1], reverse=True)
    regiones = [item[0] for item in regiones_ordenadas]
    areas = [item[1] for item in regiones_ordenadas]

    plt.figure(figsize=(10, 6))
    plt.bar(regiones, areas)
    plt.title("Área total por región")
    plt.xlabel("Región")
    plt.ylabel("Área total (km²)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(carpeta_salida / "03_area_total_por_region.png", dpi=150)
    plt.close()


def grafica_dispersion_area_vs_poblacion(datos, carpeta_salida):
    areas = [pais.get("area", 0) for pais in datos if pais.get("area", 0) > 0 and pais.get("poblacion", 0) > 0]
    poblaciones = [pais.get("poblacion", 0) for pais in datos if pais.get("area", 0) > 0 and pais.get("poblacion", 0) > 0]

    plt.figure(figsize=(9, 6))
    plt.scatter(areas, poblaciones, alpha=0.6)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Relación área vs población (escala log-log)")
    plt.xlabel("Área (km², escala log)")
    plt.ylabel("Población (escala log)")
    plt.tight_layout()
    plt.savefig(carpeta_salida / "04_dispersion_area_vs_poblacion.png", dpi=150)
    plt.close()


def grafica_top10_paises_mas_poblados(datos, carpeta_salida):
    top10 = sorted(datos, key=lambda pais: pais.get("poblacion", 0), reverse=True)[:10]
    nombres = [pais.get("nombre", "Sin nombre") for pais in top10]
    poblaciones = [pais.get("poblacion", 0) for pais in top10]

    plt.figure(figsize=(10, 7))
    plt.barh(nombres[::-1], poblaciones[::-1])
    plt.title("Top 10 países más poblados")
    plt.xlabel("Población")
    plt.ylabel("País")
    plt.tight_layout()
    plt.savefig(carpeta_salida / "05_top10_paises_mas_poblados.png", dpi=150)
    plt.close()


def grafica_mapa_calor_correlacion(datos, carpeta_salida):
    poblaciones = []
    areas = []
    densidades = []

    for pais in datos:
        poblacion = pais.get("poblacion", 0)
        area = pais.get("area", 0)
        if poblacion > 0 and area > 0:
            poblaciones.append(poblacion)
            areas.append(area)
            densidades.append(poblacion / area)

    matriz = np.array([poblaciones, areas, densidades], dtype=float)
    correlacion = np.corrcoef(matriz)
    etiquetas = ["Población", "Área", "Densidad"]

    plt.figure(figsize=(7, 6))
    imagen = plt.imshow(correlacion, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(imagen, label="Correlación")
    plt.xticks(range(len(etiquetas)), etiquetas)
    plt.yticks(range(len(etiquetas)), etiquetas)
    plt.title("Mapa de calor de correlación entre variables")

    for fila in range(correlacion.shape[0]):
        for columna in range(correlacion.shape[1]):
            valor = correlacion[fila, columna]
            plt.text(columna, fila, f"{valor:.2f}", ha="center", va="center", color="black")

    plt.tight_layout()
    plt.savefig(carpeta_salida / "06_mapa_calor_correlacion.png", dpi=150)
    plt.close()


def grafica_mapa_calor_metricas_por_region(datos, carpeta_salida):
    acumulados = defaultdict(lambda: {"poblacion": 0, "area": 0.0, "conteo": 0})

    for pais in datos:
        region = pais.get("region", "Sin región")
        acumulados[region]["poblacion"] += pais.get("poblacion", 0)
        acumulados[region]["area"] += pais.get("area", 0)
        acumulados[region]["conteo"] += 1

    regiones = sorted(acumulados.keys())
    matriz = []

    for region in regiones:
        conteo = acumulados[region]["conteo"]
        poblacion_media = acumulados[region]["poblacion"] / conteo if conteo else 0
        area_media = acumulados[region]["area"] / conteo if conteo else 0
        densidad_media = poblacion_media / area_media if area_media > 0 else 0
        matriz.append([poblacion_media, area_media, densidad_media])

    matriz_np = np.array(matriz, dtype=float)
    matriz_log = np.log10(matriz_np + 1)

    plt.figure(figsize=(9, 6))
    imagen = plt.imshow(matriz_log, cmap="YlOrRd", aspect="auto")
    plt.colorbar(imagen, label="log10(valor + 1)")
    plt.xticks(range(3), ["Pob. media", "Área media", "Densidad media"])
    plt.yticks(range(len(regiones)), regiones)
    plt.title("Mapa de calor de métricas promedio por región")

    for fila in range(matriz_log.shape[0]):
        for columna in range(matriz_log.shape[1]):
            valor_real = matriz_np[fila, columna]
            plt.text(columna, fila, f"{valor_real:,.0f}", ha="center", va="center", color="black", fontsize=8)

    plt.tight_layout()
    plt.savefig(carpeta_salida / "07_mapa_calor_metricas_por_region.png", dpi=150)
    plt.close()


def grafica_pastel_paises_por_region(datos, carpeta_salida):
    conteo = Counter(pais.get("region", "Sin región") for pais in datos)
    regiones_ordenadas = sorted(conteo.items(), key=lambda item: item[1], reverse=True)

    etiquetas = [item[0] for item in regiones_ordenadas]
    valores = [item[1] for item in regiones_ordenadas]

    plt.figure(figsize=(8, 8))
    plt.pie(
        valores,
        labels=etiquetas,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.8,
    )
    plt.title("Distribución de países por región (pastel)")
    plt.tight_layout()
    plt.savefig(carpeta_salida / "08_pastel_paises_por_region.png", dpi=150)
    plt.close()


def main():
    ruta_json = Path("JSON") / "paises_transformados.json"
    carpeta_salida = Path("GRAFICAS")
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    datos = cargar_datos(ruta_json)

    grafica_cantidad_paises_por_region(datos, carpeta_salida)
    grafica_poblacion_total_por_region(datos, carpeta_salida)
    grafica_area_total_por_region(datos, carpeta_salida)
    grafica_dispersion_area_vs_poblacion(datos, carpeta_salida)
    grafica_top10_paises_mas_poblados(datos, carpeta_salida)
    grafica_mapa_calor_correlacion(datos, carpeta_salida)
    grafica_mapa_calor_metricas_por_region(datos, carpeta_salida)
    grafica_pastel_paises_por_region(datos, carpeta_salida)

    print(f"Gráficas generadas en: {carpeta_salida.resolve()}")


if __name__ == "__main__":
    main()
