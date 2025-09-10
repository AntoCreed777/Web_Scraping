"""Script principal para el scraping de series de TV desde Sensacine."""

import logging
from typing import Optional

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


def scraping_obtener_links_series(
    desde_pagina: Optional[int] = 1, hasta_pagina: Optional[int] = None
) -> list[DatosSerie]:
    """Obtiene los links de las series de TV desde Sensacine entre las páginas indicadas."""
    series: list[DatosSerie] = []
    link_paginas_a_buscar_base = settings.series_tv_link + "?page="

    if desde_pagina is None:
        contador_paginas = 1
    else:
        contador_paginas = desde_pagina

    series_en_pagina_anterior = None

    while True:
        if hasta_pagina is not None and contador_paginas == hasta_pagina + 1:
            break

        logging.info(f"Se va a leer la pagina {contador_paginas}.")
        link_pagina_a_buscar_actual = link_paginas_a_buscar_base + str(contador_paginas)

        try:
            series_en_pagina = buscar_links_de_series(
                soup=get_soup(link=link_pagina_a_buscar_actual)
            )
        except Exception as e:
            logging.error(f"Error al obtener links de la página {contador_paginas}: {e}")
            break

        if not series_en_pagina:
            logging.error(
                f"No hay series en la pagina actual.\tSe asume que en las siguientes tampoco habra mas."
            )
            break

        if series_en_pagina_anterior is not None and series_en_pagina_anterior == series_en_pagina:
            # Si la página actual es igual a la anterior, se detiene el bucle
            break

        series += series_en_pagina
        series_en_pagina_anterior = series_en_pagina
        contador_paginas += 1

    return series


def main():
    """Función principal del script. Orquesta el scraping y muestra resultados."""
    desde_pagina: Optional[int] = 1
    hasta_pagina: Optional[int] = 150
    series = scraping_obtener_links_series(desde_pagina=desde_pagina, hasta_pagina=hasta_pagina)

    if not series:
        print("No hay series a para extraer los datos")
        exit(1)

    logging.info("SE EXTRAERAN LOS DATOS DE LAS SERIES")

    extraer_datos_de_series(series)
    df = datos_series_a_dataframe(series)
    df = limpiar_dataframe(df)

    # Creacion del nombre definitivo del archivo
    if desde_pagina is None:
        desde_pagina = 1

    if hasta_pagina is None:
        hasta_pagina = "X"

    nombre_archivo = settings.nombre_archivo_pkl
    partes_nombre_archivo = nombre_archivo.split(".")
    nombre_archivo = (
        partes_nombre_archivo[0] + f"_{desde_pagina}_{hasta_pagina}." + partes_nombre_archivo[1]
    )

    guardar_dataframe_pickle(df, nombre_archivo)
    logging.info(f"Datos guardados en {nombre_archivo}. Total de series: {len(df)}")


if __name__ == "__main__":
    main()
