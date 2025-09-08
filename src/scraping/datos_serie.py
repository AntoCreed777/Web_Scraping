"""Definición de la clase DatosSerie para almacenar información de series de TV."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SerieColumn(Enum):
    LINK = "link"
    TITULO = "titulo"
    TITULO_ORIGINAL = "titulo_original"
    GENEROS = "generos"
    CANTIDAD_TEMPORADAS = "cantidad_temporadas"
    CANTIDAD_EPISODIOS_TOTALES = "cantidad_episodios_totales"
    FECHA_EMISION_ORIGINAL = "fecha_emision_original"
    FECHA_EMISION_ULTIMA = "fecha_emision_ultima"
    PUNTUACION = "puntuacion"
    DONDE_VER = "donde_ver"


@dataclass
class DatosSerie:
    """Modelo de datos para almacenar información relevante de una serie de TV."""

    link: str

    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    generos: Optional[list[str]] = field(default_factory=list)
    cantidad_temporadas: Optional[int] = None
    cantidad_episodios_totales: Optional[int] = None
    fecha_emision_original: Optional[int] = None
    fecha_emision_ultima: Optional[int] = None
    puntuacion: Optional[float] = None
    donde_ver: Optional[list[str]] = field(default_factory=list)

    def to_dict(self):
        """Convierte el objeto DatosSerie en un diccionario usando los campos del dataclass."""
        result = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if field in (SerieColumn.GENEROS.value, SerieColumn.DONDE_VER.value):
                value = ", ".join(value) if value else None
            result[field] = value
        return result

    def __str__(self):
        """Representación en texto de los datos de la serie."""
        fecha_ini = (
            str(self.fecha_emision_original) if self.fecha_emision_original else "Desconocido"
        )
        fecha_fin = (
            str(self.fecha_emision_ultima)
            if self.fecha_emision_ultima
            else "En emisión o desconocido"
        )
        return (
            f"Título: {self.titulo or 'Desconocido'}\n"
            f"Título original: {self.titulo_original or 'Desconocido'}\n"
            f"Géneros: {', '.join(self.generos) if self.generos else 'Ninguno'}\n"
            f"Temporadas: {self.cantidad_temporadas or 'Desconocido'}\n"
            f"Episodios totales: {self.cantidad_episodios_totales or 'Desconocido'}\n"
            f"Fecha emisión: {fecha_ini} - {fecha_fin}\n"
            f"Puntuación: {self.puntuacion if self.puntuacion is not None else 'No disponible'}\n"
            f"Ver en: {', '.join(self.donde_ver) if self.donde_ver else 'No disponible'}\n"
            f"Link: {self.link}"
        )
