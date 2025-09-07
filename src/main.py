"""Script principal para el scraping de series de TV desde Sensacine."""

import logging

from const import settings
from data_frame import (
    datos_series_a_dataframe,
    guardar_dataframe_pickle,
    limpiar_dataframe,
)
from datos_serie import DatosSerie
from extraer_datos import extraer_datos_de_series
from request import buscar_links_de_series, get_soup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    """Función principal del script. Orquesta el scraping y muestra resultados."""
    series: list[DatosSerie] = buscar_links_de_series(soup=get_soup(link=settings.series_tv_link))
    extraer_datos_de_series(series)
    df = datos_series_a_dataframe(series)
    df = limpiar_dataframe(df)

    nombre_archivo = settings.nombre_archivo_pkl
    guardar_dataframe_pickle(df, nombre_archivo)
    logging.info(f"Datos guardados en {nombre_archivo}. Total de series: {len(df)}")


if __name__ == "__main__":
    main()
