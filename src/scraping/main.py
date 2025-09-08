"""Script principal para el scraping de series de TV desde Sensacine."""

import logging

from const import settings
from data_frame import (
    datos_series_a_dataframe,
    guardar_dataframe_pickle,
    limpiar_dataframe,
)
from extraer_datos import extraer_datos_de_series
from request import buscar_links_de_series, get_soup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    """Función principal del script. Orquesta el scraping y muestra resultados."""
    series = []
    link_paginas_a_buscar_base = settings.series_tv_link + "?page="
    contador_paginas = 1
    limite_de_paginas_a_analizar = 150
    series_en_pagina_anterior = None

    while True:
        if contador_paginas == limite_de_paginas_a_analizar + 1:
            break

        logging.info(f"Se va a leer la pagina {contador_paginas}.")
        link_pagina_a_buscar_actual = link_paginas_a_buscar_base + str(contador_paginas)

        try:
            series_en_pagina = buscar_links_de_series(
                soup=get_soup(link=link_pagina_a_buscar_actual)
            )
        except ValueError as e:
            print(e)
            break

        if not series_en_pagina:
            break

        if series_en_pagina_anterior is not None and series_en_pagina_anterior == series_en_pagina:
            # Si la página actual es igual a la anterior, se detiene el bucle
            break

        series += series_en_pagina
        series_en_pagina_anterior = series_en_pagina
        contador_paginas += 1

    if not series:
        print("No hay series a para extraer los datos")
        exit(1)

    logging.info("SE EXTRAERAN LOS DATOS DE LAS SERIES")

    extraer_datos_de_series(series)
    df = datos_series_a_dataframe(series)
    df = limpiar_dataframe(df)

    nombre_archivo = settings.nombre_archivo_pkl
    guardar_dataframe_pickle(df, nombre_archivo)
    logging.info(f"Datos guardados en {nombre_archivo}. Total de series: {len(df)}")


if __name__ == "__main__":
    main()
