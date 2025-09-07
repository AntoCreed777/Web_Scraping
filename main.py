import requests
from bs4 import BeautifulSoup

from const import settings


def get_soup() -> BeautifulSoup:
    try:
        r = requests.get(settings.series_tv_link)
        r.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error al realizar el request: {e}")

    return BeautifulSoup(r.content, "html.parser")


def buscar_links_de_peliculas(soup: BeautifulSoup) -> list[dict[str, str]]:
    # Busca los contenedores de películas.
    peliculas = soup.find_all("li", class_="mdl")
    links = []

    for peli in peliculas:
        # Buscar el <a> dentro de <h2> con clase 'meta-title-link'
        link = peli.find("a", class_="meta-title-link")

        if link:

            titulo = link.get_text(strip=True)
            url = link["href"]
            links.append({"titulo": titulo, "url": url})
            print(f"Título: {titulo} - URL: {settings.base_url + url}")

    return links


def main():
    soup = get_soup()

    buscar_links_de_peliculas(soup)


if __name__ == "__main__":
    main()
