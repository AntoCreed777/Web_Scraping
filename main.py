from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from const import settings
from datos_serie import DatosSerie


def get_soup(link: str) -> BeautifulSoup:
    try:
        r = requests.get(link)
        r.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error al realizar el request: {e}")

    return BeautifulSoup(r.content, "html.parser")


def buscar_links_de_series(soup: BeautifulSoup) -> list[DatosSerie]:
    # Busca los contenedores de películas.
    peliculas = soup.find_all("li", class_="mdl")
    datos_serie = []

    for peli in peliculas:
        # Buscar el <a> dentro de <h2> con clase 'meta-title-link'
        link = peli.find("a", class_="meta-title-link")

        if link:
            titulo = link.get_text(strip=True)
            href = link["href"]
            url_completa = urljoin(settings.base_url, href)
            datos_serie.append(DatosSerie(link=url_completa, titulo=titulo))

    return datos_serie


def extraer_generos(info) -> list[str]:
    div = info.find("div", class_="meta-body-info")
    if not div:
        return []

    generos_sin_procesar = div.find_all(["a", "span"], class_="dark-grey-link")
    return [g.get_text(strip=True) for g in generos_sin_procesar]


def extraer_titulo_original(info) -> str | None:
    div = info.find("div", class_="meta-body-original-title")
    if not div:
        return None

    return div.find("strong").get_text(strip=True)


def extraer_cantidad_temporadas_y_episodios(soup: BeautifulSoup) -> list[int] | None:
    info_serie_stats = soup.find("div", class_="stats-numbers-seriespage")
    if not info_serie_stats:
        return None

    div = info_serie_stats.find_all("div", class_="stats-item")
    if not div:
        return None

    return [int(d.get_text(strip=True).split()[0]) for d in div]


def extraer_donde_ver(soup: BeautifulSoup) -> list[str] | None:
    div = soup.find_all("div", class_="provider-tile-primary")
    if not div:
        return None

    return [d.get_text(strip=True) for d in div]


def extraer_datos_de_serie(serie: DatosSerie):
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
    for serie in series:
        extraer_datos_de_serie(serie=serie)
        print(serie)


def main():
    series: list[DatosSerie] = buscar_links_de_series(soup=get_soup(link=settings.series_tv_link))

    extraer_datos_de_series(series)


if __name__ == "__main__":
    main()
