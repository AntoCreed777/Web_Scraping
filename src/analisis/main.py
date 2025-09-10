"""Módulo principal de análisis para el proyecto de Web Scraping de series de TV."""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
from utilities import importar_data_frame, imprimir_data_frame, split_df

# Para poder importar de src.scraping
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scraping.datos_serie import SerieColumn, SerieNullValues


###
# ¿Cuáles servicios de streaming están como opciones disponibles para
# ver series en la lista de sensacine?
# ¿Cuántas series pueden verse en cada servicio de streaming según
# la lista de sensacine?
def respuesta_donde_ver(df: pd.DataFrame):
    """Muestra una tabla con la cantidad de series disponibles en cada servicio de streaming."""
    DONDE_VER_SPLIT, df_exploded = split_df(df, SerieColumn.DONDE_VER.value)
    conteo = df_exploded[DONDE_VER_SPLIT].value_counts()
    tabla = conteo.reset_index()
    tabla.columns = ["Servicio", "Cantidad"]
    imprimir_data_frame(tabla, mensaje="Tabla de cantidad de series por servicio de streaming:")


###
# ¿Como se distribuye la cantidad de géneros en este conjunto de series?
# Ademas, con esta información construya un gráfico de barras.
# Para esto pueden utilizar la librería **Matplotlib**.
def respuesta_generos(df: pd.DataFrame):
    """Analiza y grafica la distribución de géneros en el conjunto de series."""
    GENEROS_SPLIT, df_exploded = split_df(df, SerieColumn.GENEROS.value)

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
    """Muestra una tabla con las 30 series con más de 2 temporadas y mayor puntaje de usuarios."""
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
    """Calcula el puntaje promedio por género y muestra estadísticas descriptivas de los géneros con mayor y menor puntaje."""
    GENEROS_SPLIT, df_exploded = split_df(df, SerieColumn.GENEROS.value)

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

        # Calculo de la desviacion estandar
        desv = puntajes.std()
        if pd.isna(desv):
            desv_str = "No aplica"
        else:
            desv_str = f"{desv:.3f}"

        print(f"\nGénero: {genero}")
        print(f"Promedio: {puntajes.mean():.3f}")
        print(f"Desviación estándar: {desv_str}")
        print(f"Máximo: {puntajes.max():.3f}")
        print(f"Mínimo: {puntajes.min():.3f}")


###
# Entregue una tabla con los servicios de streaming,
# la cantidad de series que se pueden observar en cada uno de ellos y
# el puntaje por usuario promedio de estas series, redondée a 3 decimales.
def respuesta_streaming_cant_series_puntaje(df: pd.DataFrame):
    """Muestra una tabla con la cantidad de series y el puntaje promedio por servicio de streaming."""
    DONDE_VER_SPLIT, df_exploded = split_df(df, SerieColumn.DONDE_VER.value)

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
    """Filtra y muestra series con puntaje entre 3.5 y 5, género Drama, 2+ temporadas, terminadas y disponibles en streaming."""
    from datetime import datetime

    # Filtrar por puntaje
    df_filtrado = df[
        (df[SerieColumn.PUNTUACION.value] >= 3.5) & (df[SerieColumn.PUNTUACION.value] <= 5)
    ].copy()

    GENEROS_SPLIT, df_exploded = split_df(df_filtrado, SerieColumn.GENEROS.value)

    # Filtrar por género Drama
    df_exploded = df_exploded[df_exploded[GENEROS_SPLIT] == "Drama"]

    # Filtrar por temporadas
    df_exploded = df_exploded[df_exploded[SerieColumn.CANTIDAD_TEMPORADAS.value] >= 2]

    # Filtrar por series terminadas
    df_exploded = df_exploded[
        (df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value].notnull())
        & (
            df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value].astype(int)
            != SerieNullValues.FECHA_EMISION_ULTIMA.value
        )
        & (df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value].astype(int) > 1900)
        & (df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value].astype(int) <= datetime.now().year)
    ]

    # Filtrar por disponibilidad en streaming (excluye cualquier "No disponible")
    df_exploded = df_exploded[
        (df_exploded[SerieColumn.DONDE_VER.value].notnull())
        & (~df_exploded[SerieColumn.DONDE_VER.value].str.contains(SerieNullValues.DONDE_VER.value))
    ]

    # Eliminar duplicados por serie y plataforma
    df_exploded = df_exploded.drop_duplicates(
        subset=[
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.CANTIDAD_TEMPORADAS.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
            SerieColumn.DONDE_VER.value,
        ]
    )

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
    """Calcula y muestra la mejor plataforma de streaming según calidad y cantidad de series."""
    DONDE_VER_SPLIT, df_exploded = split_df(df, SerieColumn.DONDE_VER.value)

    df_exploded = df_exploded[
        (df_exploded[DONDE_VER_SPLIT].notnull())
        & (~df_exploded[SerieColumn.DONDE_VER.value].str.contains(SerieNullValues.DONDE_VER.value))
    ]

    # Se agrupa por Servicio de Streaming
    df_agrupado = df_exploded.groupby(DONDE_VER_SPLIT)

    # Calcular cantidad de series
    cantidad_series = df_agrupado[SerieColumn.TITULO.value].count()

    # Calcular puntaje promedio por servicio
    puntaje_por_servicio = df_agrupado[SerieColumn.PUNTUACION.value].mean()

    # Normalizar ambos valores (min-max)
    min_cant, max_cant = cantidad_series.min(), cantidad_series.max()
    min_punt, max_punt = puntaje_por_servicio.min(), puntaje_por_servicio.max()
    cantidad_series_norm = (
        (cantidad_series - min_cant) / (max_cant - min_cant)
        if max_cant > min_cant
        else cantidad_series * 0
    )
    puntaje_por_servicio_norm = (
        (puntaje_por_servicio - min_punt) / (max_punt - min_punt)
        if max_punt > min_punt
        else puntaje_por_servicio * 0
    )

    # Índice ponderado
    alpha = 0.5
    beta = 0.5
    indice_ponderado = alpha * puntaje_por_servicio_norm + beta * cantidad_series_norm

    # Crear la tabla
    tabla = pd.DataFrame(
        {
            "Streaming": cantidad_series.index,
            "Cantidad de series": cantidad_series.values,
            "Puntaje promedio": puntaje_por_servicio.values,
            "Índice calidad*cantidad (ponderado)": indice_ponderado.values,
        }
    )

    # Ordenar por índice ponderado
    tabla = tabla.sort_values(by="Índice calidad*cantidad (ponderado)", ascending=False)

    imprimir_data_frame(
        tabla,
        mensaje="Mejor plataforma de streaming según índice calidad*cantidad (normalizado y ponderado):",
    )


###
# Entregue una tabla con series que tengan una puntuacion por usuarios
# entre mínimo 4 y máximo 5.0, que tenga como género Animación, que hayan
# sido emitidas durante el ultimo año (2025) y pueda verse en una
# plataforma de streaming.
def respuesta_series_puntaje_4_5_animacion_ultimo_ano_ver(df: pd.DataFrame):
    """Muestra series de animación con puntaje entre 4 y 5, emitidas en el último año y disponibles en streaming."""
    # Filtrar por puntaje
    df_filtrado = df[
        (df[SerieColumn.PUNTUACION.value] >= 4) & (df[SerieColumn.PUNTUACION.value] <= 5)
    ].copy()

    GENEROS_SPLIT, df_exploded = split_df(df_filtrado, SerieColumn.GENEROS.value)

    # Filtrar por género Animación
    df_exploded = df_exploded[df_exploded[GENEROS_SPLIT] == "Animación"]

    # Filtrar por series emitidas en 2025
    df_exploded = df_exploded[df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value] == 2025]

    # Filtrar por disponibilidad en streaming
    df_exploded = df_exploded[
        (df_exploded[SerieColumn.DONDE_VER.value].notnull())
        & (~df_exploded[SerieColumn.DONDE_VER.value].str.contains(SerieNullValues.DONDE_VER.value))
    ]

    # Mostrar tabla
    imprimir_data_frame(
        df_exploded,
        mensaje="Tabla de series de animación con puntaje entre 4 y 5, emitidas en 2025 y disponibles en streaming:",
        columnas=[
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
            SerieColumn.DONDE_VER.value,
        ],
    )


###
# En base a tu analisis ¿Que serie de animación reciente
# recomendarias a un fan de la acción?
# ¿Para un fan de la comedia?
def respuesta_recomendacion(df: pd.DataFrame):
    """Recomienda series de animación recientes para fans de acción y comedia."""
    GENEROS_SPLIT, df_exploded = split_df(df, SerieColumn.GENEROS.value)

    # Filtrar series de animación emitidas en el último año (2025)
    df_animacion_2025 = df_exploded[
        (df_exploded[GENEROS_SPLIT] == "Animación")
        & (df_exploded[SerieColumn.FECHA_EMISION_ULTIMA.value] == 2025)
    ]

    # Buscar series que también tengan Acción
    df_accion = df_animacion_2025[
        df_animacion_2025[SerieColumn.GENEROS.value].str.contains("Acción")
    ]

    # Buscar series que también tengan Comedia
    df_comedia = df_animacion_2025[
        df_animacion_2025[SerieColumn.GENEROS.value].str.contains("Comedia")
    ]

    # Ordenar por puntaje descendente
    df_accion_sorted = df_accion.sort_values(by=SerieColumn.PUNTUACION.value, ascending=False)
    df_comedia_sorted = df_comedia.sort_values(by=SerieColumn.PUNTUACION.value, ascending=False)

    # Mostrar recomendación para fans de acción
    imprimir_data_frame(
        df_accion_sorted,
        mensaje="Recomendación de series de animación recientes para fans de la acción (ordenadas por puntaje):",
        columnas=[
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
            SerieColumn.DONDE_VER.value,
        ],
    )

    # Mostrar recomendación para fans de comedia
    imprimir_data_frame(
        df_comedia_sorted,
        mensaje="Recomendación de series de animación recientes para fans de la comedia (ordenadas por puntaje):",
        columnas=[
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
            SerieColumn.DONDE_VER.value,
        ],
    )


###
# Entregue una tabla con series con la serie mejor evaluada
# por cada año segun su fecha original de emisión.
def respuesta_series_mejor_evaluadas_por_anio(df: pd.DataFrame):
    """Muestra la serie mejor evaluada por cada año de emisión original."""
    from datetime import datetime

    # Agrupar por año de emisión original y obtener la serie con mayor puntaje en cada año
    df_filtrado = df[
        (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].notnull())
        & (
            df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int)
            != SerieNullValues.FECHA_EMISION_ORIGINAL.value
        )
        & (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int) > 1900)
        & (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int) <= datetime.now().year)
    ]
    idx = df_filtrado.groupby(SerieColumn.FECHA_EMISION_ORIGINAL.value)[
        SerieColumn.PUNTUACION.value
    ].idxmax()

    # Eliminar posibles NaN en idx para evitar KeyError
    idx = idx.dropna()
    df_mejor_por_anio = df_filtrado.loc[idx]

    # Mostrar tabla ordenada por año
    df_mejor_por_anio = df_mejor_por_anio.sort_values(by=SerieColumn.FECHA_EMISION_ORIGINAL.value)
    imprimir_data_frame(
        df_mejor_por_anio,
        mensaje="Tabla de la serie mejor evaluada por cada año de emisión original:",
        columnas=[
            SerieColumn.FECHA_EMISION_ORIGINAL.value,
            SerieColumn.TITULO.value,
            SerieColumn.PUNTUACION.value,
            SerieColumn.GENEROS.value,
            SerieColumn.DONDE_VER.value,
        ],
    )


###
# Presente un histograma con el puntaje promedio de
# las series estrenadas durante ese año por cada año.
def respuesta_puntaje_promedio_por_anio(df: pd.DataFrame):
    """Presenta un histograma con el puntaje promedio de las series estrenadas por año."""
    from datetime import datetime

    df_filtrado = df[
        (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].notnull())
        & (
            df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int)
            != SerieNullValues.FECHA_EMISION_ORIGINAL.value
        )
        & (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int) > 1900)
        & (df[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int) <= datetime.now().year)
    ]

    df_agrupado = df_filtrado.groupby(SerieColumn.FECHA_EMISION_ORIGINAL.value)[
        SerieColumn.PUNTUACION.value
    ].mean()
    df_tabla = df_agrupado.reset_index()

    # Graficar puntaje promedio por año (gráfico de barras)
    plt.figure(figsize=(12, 6))
    anios = df_tabla[SerieColumn.FECHA_EMISION_ORIGINAL.value].astype(int)
    plt.bar(anios, df_tabla[SerieColumn.PUNTUACION.value], color="skyblue", edgecolor="black")
    plt.xlabel("Año")
    plt.ylabel("Puntaje promedio")
    plt.title("Puntaje promedio de series estrenadas por año")
    plt.xticks(anios, rotation=45)
    plt.tight_layout()
    # plt.show()
    plt.savefig("puntaje_promedio_por_año.png")
    print("Grafico generado")


def main():
    """Ejecuta el análisis principal sobre el DataFrame de series de TV."""
    df = importar_data_frame()

    print("\nParte 2.1")
    respuesta_donde_ver(df)

    print("\nParte 2.2")
    respuesta_generos(df)

    print("\nParte 2.3")
    respuesta_series_con_mas_temporadas_puntaje(df)
    respuesta_puntaje_generos_estadisticas(df)
    respuesta_streaming_cant_series_puntaje(df)

    print("\nParte 2.4")
    respuesta_series_puntuacion_en_limites(df)
    respuesta_mejor_plataforma_streaming(df)

    print("\nParte 2.5")
    respuesta_series_puntaje_4_5_animacion_ultimo_ano_ver(df)
    respuesta_recomendacion(df)

    print("\nParte 2.6")
    respuesta_series_mejor_evaluadas_por_anio(df)
    respuesta_puntaje_promedio_por_anio(df)


if __name__ == "__main__":
    main()
