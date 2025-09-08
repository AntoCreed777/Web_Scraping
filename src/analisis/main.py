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

    print(df_exploded[DONDE_VER_SPLIT].unique())

    # Contar cuántas series hay por cada servicio
    conteo = df_exploded[DONDE_VER_SPLIT].value_counts()
    print(conteo)


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


def main():
    df = importar_data_frame()

    respuesta_donde_ver(df)

    respuesta_generos(df)


if __name__ == "__main__":
    main()
