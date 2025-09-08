import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scraping.const import settings
from src.scraping.datos_serie import SerieColumn


def importar_data_frame() -> pd.DataFrame:
    return pd.read_pickle(settings.nombre_archivo_pkl)


def respuesta_donde_ver(df: pd.DataFrame):
    DONDE_VER_SPLIT = "donde_ver_split"

    # Separar los servicios en listas
    df[DONDE_VER_SPLIT] = df[SerieColumn.DONDE_VER.value].str.split(",")

    # Explode para tener una fila por cada servicio
    df_exploded = df.explode(DONDE_VER_SPLIT)

    # Limpiar espacios extra
    df_exploded[DONDE_VER_SPLIT] = df_exploded[DONDE_VER_SPLIT].str.strip()

    # Contar cuántas series hay por cada servicio
    conteo = df_exploded[DONDE_VER_SPLIT].value_counts()

    tabla = conteo.reset_index()
    tabla.columns = ["Servicio", "Cantidad"]
    print(tabla.to_markdown(index=False))


def respuesta_generos(df: pd.DataFrame):
    GENEROS_SPLIT = "generos_split"

    # Separar los géneros en listas
    df[GENEROS_SPLIT] = df[SerieColumn.GENEROS.value].str.split(",")

    # Explode para tener una fila por cada género
    df_exploded = df.explode(GENEROS_SPLIT)

    # Limpiar espacios extra
    df_exploded[GENEROS_SPLIT] = df_exploded[GENEROS_SPLIT].str.strip()

    # Contar cuántas veces aparece cada género
    conteo_generos = df_exploded[GENEROS_SPLIT].value_counts()

    # Graficar la distribución de géneros
    conteo_generos.plot(kind="bar", figsize=(12, 6))
    plt.xlabel("Género")
    plt.ylabel("Cantidad")
    plt.title("Distribución de géneros en series")
    plt.tight_layout()
    # plt.show()
    plt.savefig("distribucion_generos.png")


def respuesta_series_con_mas_temporadas_puntaje(df: pd.DataFrame):
    # Filtrar series con más de 2 temporadas
    df_filtrado = df[df[SerieColumn.CANTIDAD_TEMPORADAS.value] > 2]

    # Seleccionar columnas relevantes
    columnas = [
        SerieColumn.TITULO.value,
        SerieColumn.PUNTUACION.value,
        SerieColumn.CANTIDAD_TEMPORADAS.value,
        SerieColumn.CANTIDAD_EPISODIOS_TOTALES.value,
    ]
    df_seleccion = df_filtrado[columnas]

    # Ordenar por puntaje descendente y tomar los 30 primeros
    df_top = df_seleccion.sort_values(by=SerieColumn.PUNTUACION.value, ascending=False).head(30)

    # Renombrar columnas para la tabla
    df_top = df_top.rename(
        columns={
            SerieColumn.TITULO.value: "Nombre",
            SerieColumn.PUNTUACION.value: "Puntaje de usuarios",
            SerieColumn.CANTIDAD_TEMPORADAS.value: "Temporadas",
            SerieColumn.CANTIDAD_EPISODIOS_TOTALES.value: "Episodios",
        }
    )

    print(df_top.to_markdown(index=False))


def main():
    df = importar_data_frame()

    respuesta_donde_ver(df)

    respuesta_generos(df)

    respuesta_series_con_mas_temporadas_puntaje(df)


if __name__ == "__main__":
    main()
