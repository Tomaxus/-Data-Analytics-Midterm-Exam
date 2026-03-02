import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree


def preparar_datos(ruta_archivo):
    """Lee los datos, limpia nulos y prepara X e y para clasificación."""
    print("[1/3] Leyendo y preparando datos...")

    tabla_datos = pd.read_json(ruta_archivo)

    columnas_necesarias = ["poblacion", "area", "region"]
    tabla_limpia = tabla_datos[columnas_necesarias].dropna()

    caracteristicas = tabla_limpia[["poblacion", "area"]]
    objetivo_texto = tabla_limpia["region"]

    codificador_region = LabelEncoder()
    objetivo_codificado = codificador_region.fit_transform(objetivo_texto)

    print(f"Datos listos: {len(tabla_limpia)} filas válidas.")
    return caracteristicas, objetivo_codificado, codificador_region


def entrenar_arbol(caracteristicas, objetivo):
    """Divide datos, entrena Árbol de Decisión con criterio Gini y predice."""
    print("[2/3] Entrenando modelo de Árbol de Decisión...")

    (
        caracteristicas_entrenamiento,
        caracteristicas_prueba,
        objetivo_entrenamiento,
        objetivo_prueba,
    ) = train_test_split(
        caracteristicas,
        objetivo,
        test_size=0.20,
        random_state=42,
        stratify=objetivo,
    )

    modelo_arbol = DecisionTreeClassifier(criterion="gini", random_state=42)
    modelo_arbol.fit(caracteristicas_entrenamiento, objetivo_entrenamiento)

    predicciones_prueba = modelo_arbol.predict(caracteristicas_prueba)

    print("Modelo entrenado y predicciones generadas.")
    return modelo_arbol, caracteristicas_prueba, objetivo_prueba, predicciones_prueba


def guardar_resultados(modelo, X_prueba, y_prueba, predicciones, codificador):
    """Guarda reporte de precisión y gráfico del árbol en carpeta de resultados."""
    print("[3/3] Guardando resultados del modelo...")

    carpeta_resultados = "MACHINE_LERANING"
    os.makedirs(carpeta_resultados, exist_ok=True)

    reporte_texto = classification_report(
        y_prueba,
        predicciones,
        target_names=codificador.classes_,
        zero_division=0,
    )

    ruta_reporte = os.path.join(carpeta_resultados, "reporte_precision.txt")
    with open(ruta_reporte, "w", encoding="utf-8") as archivo_reporte:
        archivo_reporte.write("REPORTE DE CLASIFICACIÓN - ÁRBOL DE DECISIÓN\n")
        archivo_reporte.write("============================================\n\n")
        archivo_reporte.write(reporte_texto)
        archivo_reporte.write("\n\n")
        archivo_reporte.write("Codificación de regiones:\n")
        for indice, etiqueta in enumerate(codificador.classes_):
            archivo_reporte.write(f"{indice}: {etiqueta}\n")

    plt.figure(figsize=(18, 10))
    plot_tree(
        modelo,
        feature_names=["poblacion", "area"],
        class_names=codificador.classes_,
        filled=True,
        rounded=True,
        fontsize=8,
    )
    plt.title("Árbol de Decisión para clasificación por región")
    plt.tight_layout()

    ruta_grafico = os.path.join(carpeta_resultados, "grafico_arbol.png")
    plt.savefig(ruta_grafico, dpi=180)
    plt.close()

    print(f"Reporte guardado en: {ruta_reporte}")
    print(f"Gráfico del árbol guardado en: {ruta_grafico}")


def main():
    ruta_archivo = os.path.join("JSON", "paises_transformados.json")

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo de entrada: {ruta_archivo}. "
            "Asegura que exista la carpeta JSON con paises_transformados.json"
        )

    X, y, codificador = preparar_datos(ruta_archivo)
    modelo, X_prueba, y_prueba, predicciones = entrenar_arbol(X, y)
    guardar_resultados(modelo, X_prueba, y_prueba, predicciones, codificador)

    print("Proceso de Machine Learning completado correctamente.")


if __name__ == '__main__':
    main()
