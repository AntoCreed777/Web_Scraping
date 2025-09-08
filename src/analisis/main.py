import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scraping.const import settings
from src.scraping.datos_serie import SerieColumn


def importar_data_frame() -> pd.DataFrame:
    return pd.read_pickle(settings.nombre_archivo_pkl)


def imprimir_data_frame(df: pd.DataFrame, mensaje: str, columnas: list[str] | None = None):
    """
    Imprime el DataFrame en formato tabla markdown.
    Si se especifica una lista de columnas, solo muestra esas columnas.
    """
    if columnas is not None:
        df = df[columnas]

    print(f"\n{mensaje}")
    print(df.to_markdown(index=False))


###
# ¿Cuáles servicios de streaming están como opciones disponibles para
# ver series en la lista de sensacine?
# ¿Cuántas series pueden verse en cada servicio de streaming según
# la lista de sensacine?
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
    imprimir_data_frame(tabla, mensaje="Tabla de cantidad de series por servicio de streaming:")


###
# ¿Como se distribuye la cantidad de géneros en este conjunto de series?
# Ademas, con esta información construya un gráfico de barras.
# Para esto pueden utilizar la librería **Matplotlib**.
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

    tabla_generos = conteo_generos.reset_index()
    tabla_generos.columns = ["Género", "Cantidad"]
    imprimir_data_frame(tabla_generos, mensaje="Tabla de cantidad de series por género:")

    # Graficar la distribución de géneros
    conteo_generos.plot(kind="bar", figsize=(12, 6))
    plt.xlabel("Género")
    plt.ylabel("Cantidad")
    plt.title("Distribución de géneros en series")
    plt.tight_layout()
    # plt.show()
    plt.savefig("distribucion_generos.png")


###
# Entregue una tabla con las 30 series con más de 2 temporadas
# y mayor puntaje hecho por usuarios.
# Muestre solamente nombre, puntaje, cantidad de temporadas y cantidad de episodios
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

    imprimir_data_frame(
        df_top, mensaje="Tabla de series con más de 2 temporadas y mayor puntaje de usuarios:"
    )


###
# Muestre en una tabla el puntaje segun usuarios promedio de todos
# los generos (redondée a 3 decimales) y luego las estadísticas descriptivas
# (desviación estándar, promedio, valor máximo y mínimo) de los 3 géneros de
# series que tengan la mayor puntuación promedio y los 2 generos que tengan
# la menor puntuación promedio.
def respuesta_puntaje_generos_estadisticas(df: pd.DataFrame):
    GENEROS_SPLIT = "generos_split"

    # Separar los géneros en listas
    df[GENEROS_SPLIT] = df[SerieColumn.GENEROS.value].str.split(",")

    # Explode para tener una fila por cada género
    df_exploded = df.explode(GENEROS_SPLIT)

    # Limpiar espacios extra
    df_exploded[GENEROS_SPLIT] = df_exploded[GENEROS_SPLIT].str.strip()

    # Calcular puntaje promedio por género
    puntaje_por_genero = (
        df_exploded.groupby(GENEROS_SPLIT)[SerieColumn.PUNTUACION.value].mean().round(3)
    )
    tabla = puntaje_por_genero.reset_index().rename(
        columns={
            GENEROS_SPLIT: "Genero",
            SerieColumn.PUNTUACION.value: "Puntaje por usuario promedio",
        }
    )

    imprimir_data_frame(tabla, mensaje="Tabla de puntaje promedio por género:")

    # Seleccionar géneros con mayor y menor puntaje promedio
    top3 = puntaje_por_genero.sort_values(ascending=False).head(3)
    bottom2 = puntaje_por_genero.sort_values(ascending=True).head(2)

    print("\nEstadísticas descriptivas de los 3 géneros con mayor puntaje promedio:")
    for genero in top3.index:
        puntajes = df_exploded[df_exploded[GENEROS_SPLIT] == genero][SerieColumn.PUNTUACION.value]
        print(f"\nGénero: {genero}")
        print(f"Promedio: {puntajes.mean():.3f}")
        print(f"Desviación estándar: {puntajes.std():.3f}")
        print(f"Máximo: {puntajes.max():.3f}")
        print(f"Mínimo: {puntajes.min():.3f}")

    print("\nEstadísticas descriptivas de los 2 géneros con menor puntaje promedio:")
    for genero in bottom2.index:
        puntajes = df_exploded[df_exploded[GENEROS_SPLIT] == genero][SerieColumn.PUNTUACION.value]
        print(f"\nGénero: {genero}")
        print(f"Promedio: {puntajes.mean():.3f}")
        print(f"Desviación estándar: {puntajes.std():.3f}")
        print(f"Máximo: {puntajes.max():.3f}")
        print(f"Mínimo: {puntajes.min():.3f}")


###
# Entregue una tabla con los servicios de streaming,
# la cantidad de series que se pueden observar en cada uno de ellos y
# el puntaje por usuario promedio de estas series, redondée a 3 decimales.
def respuesta_streaming_cant_series_puntaje(df: pd.DataFrame):
    DONDE_VER_SPLIT = "donde_ver_split"

    # Separar los servicios en listas
    df[DONDE_VER_SPLIT] = df[SerieColumn.DONDE_VER.value].str.split(",")

    # Explode para tener una fila por cada servicio
    df_exploded = df.explode(DONDE_VER_SPLIT)

    # Limpiar espacios extra
    df_exploded[DONDE_VER_SPLIT] = df_exploded[DONDE_VER_SPLIT].str.strip()

    # Se agrupa por Servicio de Streaming
    df_agrupado = df_exploded.groupby(DONDE_VER_SPLIT)

    # Calcular cantidad de series
    cantidad_series = df_agrupado[SerieColumn.TITULO.value].count()

    # Calcular puntaje promedio por servicio
    puntaje_por_servicio = df_agrupado[SerieColumn.PUNTUACION.value].mean().round(3)

    # Unir ambas métricas en una sola tabla
    tabla = pd.DataFrame(
        {
            "Streaming": cantidad_series.index,
            "Cantidad de series": cantidad_series.values,
            "Puntuacion por usuario promedio": puntaje_por_servicio.values,
        }
    )

    imprimir_data_frame(
        tabla, mensaje="Tabla de servicios de streaming, cantidad de series y puntaje promedio:"
    )


###
# Entregue una tabla con series que tengan una puntuacion
# por usuarios entre mínimo 3.5 y máximo 5.0, que tenga como género Drama,
# que tengan 2 o más Temporadas, que hayan terminado de emitirse y
# pueda verse en una plataforma de streaming.
def respuesta_series_puntuacion_en_limites(df: pd.DataFrame):
    # Filtrar por puntaje
    df_filtrado = df[
        (df[SerieColumn.PUNTUACION.value] >= 3.5) & (df[SerieColumn.PUNTUACION.value] <= 5)
    ].copy()

    GENEROS_SPLIT = "generos_split"
    df_filtrado[GENEROS_SPLIT] = df_filtrado[SerieColumn.GENEROS.value].str.split(",")
    df_exploded = df_filtrado.explode(GENEROS_SPLIT)
    df_exploded[GENEROS_SPLIT] = df_exploded[GENEROS_SPLIT].str.strip()

    # Filtrar por género Drama
    df_exploded = df_exploded[df_exploded[GENEROS_SPLIT] == "Drama"]

    # Filtrar por temporadas
    df_exploded = df_exploded[df_exploded[SerieColumn.CANTIDAD_TEMPORADAS.value] >= 2]

    # Filtrar por series terminadas
    df_exploded = df_exploded[df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value].notnull()]

    # Filtrar por disponibilidad en streaming
    df_exploded = df_exploded[
        df_exploded[SerieColumn.DONDE_VER.value].notnull()
        & (df_exploded[SerieColumn.DONDE_VER.value] != "")
    ]

    imprimir_data_frame(
        df_exploded,
        mensaje="Tabla de series con puntuación entre 3.5 y 5, género Drama, 2+ temporadas, terminadas y disponibles en streaming:",
        columnas=[
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.CANTIDAD_TEMPORADAS.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
            SerieColumn.DONDE_VER.value,
        ],
    )


###
# ¿Cúal es la plataforma de streaming que vale la pena contratar
# según calidad/cantidad de series de acuerdo con los datos de Sensacine?
def respuesta_mejor_plataforma_streaming(df: pd.DataFrame):
    pass


def main():
    df = importar_data_frame()

    # respuesta_donde_ver(df)
    # respuesta_generos(df)
    # respuesta_series_con_mas_temporadas_puntaje(df)
    # respuesta_puntaje_generos_estadisticas(df)
    # respuesta_series_puntuacion_en_limites(df)
    respuesta_mejor_plataforma_streaming(df)


if __name__ == "__main__":
    main()
