"""Funciones para obtener y buscar series desde Sensacine usando requests y BeautifulSoup."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from const import settings
from datos_serie import DatosSerie


def get_soup(link: str) -> BeautifulSoup:
    """Obtiene y parsea el contenido HTML de un enlace usando BeautifulSoup.

    Args:
        link (str): URL a consultar.

    Returns:
        BeautifulSoup: Objeto parseado del HTML.

    Raises:
        ValueError: Si ocurre un error en la petición HTTP.
    """
    try:
        r = requests.get(link)
        r.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error al realizar el request: {e}")

    return BeautifulSoup(r.content, "html.parser")


def buscar_links_de_series(soup: BeautifulSoup) -> list[DatosSerie]:
    """Busca y retorna los links y títulos de series en el HTML dado.

    Args:
        soup (BeautifulSoup): HTML parseado de la página principal.

    Returns:
        list[DatosSerie]: Lista de objetos DatosSerie con link y título.
    """
    # Busca los contenedores de películas.
    peliculas = None
    try:
        peliculas = soup.find_all("li", class_="mdl")
    except Exception as e:
        raise e

    datos_serie = []

    for peli in peliculas:
        link = peli.find("a", class_="meta-title-link")

        if link:
            titulo = link.get_text(strip=True)
            href = link["href"]
            url_completa = urljoin(settings.base_url, href)
            datos_serie.append(DatosSerie(link=url_completa, titulo=titulo))

    return datos_serie
