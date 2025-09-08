"""Definición de la clase DatosSerie para almacenar información de series de TV."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatosSerie:
    """Modelo de datos para almacenar información relevante de una serie de TV."""

    link: str

    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    genero: Optional[str] = None
    sub_generos: Optional[list[str]] = field(default_factory=list)
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
            if field in ("sub_generos", "donde_ver"):
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
            f"Género principal: {self.genero or 'Desconocido'}\n"
            f"Subgéneros: {', '.join(self.sub_generos) if self.sub_generos else 'Ninguno'}\n"
            f"Temporadas: {self.cantidad_temporadas or 'Desconocido'}\n"
            f"Episodios totales: {self.cantidad_episodios_totales or 'Desconocido'}\n"
            f"Fecha emisión: {fecha_ini} - {fecha_fin}\n"
            f"Puntuación: {self.puntuacion if self.puntuacion is not None else 'No disponible'}\n"
            f"Ver en: {', '.join(self.donde_ver) if self.donde_ver else 'No disponible'}\n"
            f"Link: {self.link}"
        )
