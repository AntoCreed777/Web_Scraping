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


def extraer_cantidad_temporadas_y_episodios(soup: BeautifulSoup) -> tuple[int | None, int | None]:
    """
    Extrae la cantidad de temporadas y episodios de la serie.

    Args:
        soup (BeautifulSoup): HTML parseado de la página de la serie.

    Returns:
        tuple[int | None, int | None]: Una tupla (temporadas, episodios), cada uno puede ser None si no se encuentra.
    """
    info_serie_stats = soup.find("div", class_="stats-numbers-seriespage")
    if not info_serie_stats:
        return (None, None)

    divs = info_serie_stats.find_all("div", class_="stats-item")
    temporadas = None
    episodios = None
    if len(divs) > 0:
        try:
            temporadas = int(divs[0].get_text(strip=True).split()[0])
        except Exception:
            temporadas = None
    if len(divs) > 1:
        try:
            episodios = int(divs[1].get_text(strip=True).split()[0])
        except Exception:
            episodios = None
    return (temporadas, episodios)


def extraer_fecha_emision(info) -> tuple[int | None, int | None]:
    """
    Extrae las fechas de emisión original y última de la serie.

    Args:
        info (BeautifulSoup): Bloque HTML con información de la serie.

    Returns:
        tuple[int | None, int | None]: Una tupla (año_inicio, año_final), cada uno puede ser None si no se encuentra.
    """
    div = info.find("div", class_="meta-body-info")
    if not div:
        return (None, None)
    texto = div.get_text(" ", strip=True)

    import re

    # Busca patrones como "2013 - 2022" o "2013 - "
    match = re.search(r"(\d{4})\s*-\s*(\d{4})?", texto)
    if match:
        anio_inicio = int(match.group(1))
        anio_final = match.group(2)
        if anio_final and anio_final.isdigit():
            return (anio_inicio, int(anio_final))
        else:
            return (anio_inicio, None)

    # Si solo hay un año
    match = re.search(r"(\d{4})", texto)
    if match:
        return (int(match.group(1)), None)
    return (None, None)


def extraer_puntuacion(soup: BeautifulSoup) -> float | None:
    div = soup.find("span", class_="stareval-note")
    if not div:
        return None
    texto = div.get_text(strip=True)

    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return None


def extraer_donde_ver(soup: BeautifulSoup) -> list[str]:
    """Extrae las plataformas donde se puede ver la serie.

    Args:
        soup (BeautifulSoup): HTML parseado de la página de la serie.

    Returns:
        list[str]: Lista de plataformas.
    """
    div = soup.find_all("div", class_="provider-tile-primary")
    if not div:
        return []

    return [d.get_text(strip=True) for d in div]


def extraer_datos_de_serie(serie: DatosSerie):
    """Extrae y asigna todos los datos relevantes de una serie.

    Args:
        serie (DatosSerie): Objeto DatosSerie a completar.
    """
    soup = get_soup(link=serie.link)

    # Extraer Genero y Sub-Genero
    info_serie = soup.find("div", class_="meta-body")

    serie.generos = extraer_generos(info=info_serie)

    # Extraer el Titulo Original
    serie.titulo_original = extraer_titulo_original(info=info_serie)

    # Extraer cantidad de Temporadas y cantidad de Capitulos Totales
    if temporadas_y_episodios := extraer_cantidad_temporadas_y_episodios(soup=soup):
        serie.cantidad_temporadas = temporadas_y_episodios[0]
        serie.cantidad_episodios_totales = temporadas_y_episodios[1]

    # Extraer fechas de emision original y ultima
    if fechas_emision := extraer_fecha_emision(info=info_serie):
        serie.fecha_emision_original = fechas_emision[0]
        serie.fecha_emision_ultima = fechas_emision[1]

    # Extraer puntuacion
    serie.puntuacion = extraer_puntuacion(soup)

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
