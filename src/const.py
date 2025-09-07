"""Constantes y configuración para el scraping de series de TV."""

from dataclasses import dataclass


@dataclass
class AppSettings:
    """Configuración de la aplicación para URLs base y endpoints."""

    base_url: str = "https://www.sensacine.com/"

    @property
    def series_tv_link(self):
        """Devuelve el enlace completo para la sección de series de TV."""
        return self.base_url + "series-tv/"


settings = AppSettings()
