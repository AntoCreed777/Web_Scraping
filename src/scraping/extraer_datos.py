"""Funciones para extraer información detallada de series desde Sensacine."""

import logging

from bs4 import BeautifulSoup
from datos_serie import DatosSerie
from request import get_soup


def extraer_generos(info) -> list[str]:
    """Extrae los géneros de una serie desde el bloque de información.

    Args:
        info (BeautifulSoup): Bloque HTML con información de la serie.

    Returns:
        list[str]: Lista de géneros encontrados.
    """
    div = info.find("div", class_="meta-body-info")
    if not div:
        return []

    generos_sin_procesar = div.find_all(["a", "span"], class_="dark-grey-link")
    return [g.get_text(strip=True) for g in generos_sin_procesar]


def extraer_titulo_original(info) -> str | None:
    """Extrae el título original de la serie si está disponible.

    Args:
        info (BeautifulSoup): Bloque HTML con información de la serie.

    Returns:
        str | None: Título original o None si no existe.
    """
    div = info.find("div", class_="meta-body-original-title")
    if not div:
        return None

    return div.find("strong").get_text(strip=True)


def extraer_cantidad_temporadas_y_episodios(soup: BeautifulSoup) -> list[int] | None:
    """Extrae la cantidad de temporadas y episodios de la serie.

    Args:
        soup (BeautifulSoup): HTML parseado de la página de la serie.

    Returns:
        list[int] | None: [temporadas, episodios] o None si no se encuentra.
    """
    info_serie_stats = soup.find("div", class_="stats-numbers-seriespage")
    if not info_serie_stats:
        return None

    div = info_serie_stats.find_all("div", class_="stats-item")
    if not div:
        return None

    return [int(d.get_text(strip=True).split()[0]) for d in div]


def extraer_donde_ver(soup: BeautifulSoup) -> list[str] | None:
    """Extrae las plataformas donde se puede ver la serie.

    Args:
        soup (BeautifulSoup): HTML parseado de la página de la serie.

    Returns:
        list[str] | None: Lista de plataformas o None si no hay datos.
    """
    div = soup.find_all("div", class_="provider-tile-primary")
    if not div:
        return None

    return [d.get_text(strip=True) for d in div]


def extraer_datos_de_serie(serie: DatosSerie):
    """Extrae y asigna todos los datos relevantes de una serie.

    Args:
        serie (DatosSerie): Objeto DatosSerie a completar.
    """
    soup = get_soup(link=serie.link)

    # Extraer Genero y Sub-Genero
    info_serie = soup.find("div", class_="meta-body")

    generos = extraer_generos(info=info_serie)

    if generos:
        serie.genero = generos[0]  # el principal
        serie.sub_generos = generos[1:]  # los demás

    # Extraer el Titulo Original
    serie.titulo_original = extraer_titulo_original(info=info_serie)

    # Extraer cantidad de Temporadas y cantidad de Capitulos Totales
    temporadas_y_episodios = extraer_cantidad_temporadas_y_episodios(soup=soup)

    if temporadas_y_episodios:
        serie.cantidad_temporadas = temporadas_y_episodios[0]
        serie.cantidad_episodios_totales = temporadas_y_episodios[1]

    # Extraer donde se puede ver
    serie.donde_ver = extraer_donde_ver(soup=soup)


def extraer_datos_de_series(series: list[DatosSerie]):
    """Itera sobre una lista de series y extrae sus datos.

    Args:
        series (list[DatosSerie]): Lista de series a procesar.
    """
    for serie in series:
        extraer_datos_de_serie(serie=serie)
        logging.info(serie)
