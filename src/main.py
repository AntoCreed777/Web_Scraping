"""Script principal para el scraping de series de TV desde Sensacine."""

import logging
import pickle
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from const import settings
from datos_serie import DatosSerie

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
    peliculas = soup.find_all("li", class_="mdl")
    datos_serie = []

    for peli in peliculas:
        link = peli.find("a", class_="meta-title-link")

        if link:
            titulo = link.get_text(strip=True)
            href = link["href"]
            url_completa = urljoin(settings.base_url, href)
            datos_serie.append(DatosSerie(link=url_completa, titulo=titulo))

    return datos_serie


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


def datos_series_a_dataframe(series: list[DatosSerie]) -> pd.DataFrame:
    """Convierte una lista de DatosSerie en un DataFrame de pandas."""
    data = []
    for s in series:
        data.append(s.to_dict())
    df = pd.DataFrame(data)
    return df


def limpiar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza limpieza básica del DataFrame usando los campos del dataclass."""
    for field in DatosSerie.__dataclass_fields__:
        if field == "titulo" or field == "genero":
            df[field] = df[field].fillna("Desconocido")
        elif field == "cantidad_temporadas" or field == "cantidad_episodios_totales":
            df[field] = df[field].fillna(0).astype(int)
        elif field == "donde_ver":
            df[field] = df[field].fillna("No disponible")
    return df


def guardar_dataframe_pickle(df: pd.DataFrame, filename: str):
    """Guarda el DataFrame en un archivo pickle."""
    with open(filename, "wb") as f:
        pickle.dump(df, f)


def main():
    """Función principal del script. Orquesta el scraping y muestra resultados."""
    series: list[DatosSerie] = buscar_links_de_series(soup=get_soup(link=settings.series_tv_link))
    extraer_datos_de_series(series)
    df = datos_series_a_dataframe(series)
    df = limpiar_dataframe(df)

    nombre_archivo = "series_tv.pkl"
    guardar_dataframe_pickle(df, nombre_archivo)
    logging.info(f"Datos guardados en {nombre_archivo}. Total de series: {len(df)}")


if __name__ == "__main__":
    main()
