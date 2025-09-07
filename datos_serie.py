from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatosSerie:
    link: str

    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    genero: Optional[str] = None
    sub_generos: Optional[list[str]] = field(default_factory=list)
    cantidad_temporadas: Optional[int] = None
    cantidad_episodios_totales: Optional[int] = None
    donde_ver: Optional[list[str]] = field(default_factory=list)

    def __str__(self):
        return (
            f"Título: {self.titulo or 'Desconocido'}\n"
            f"Título original: {self.titulo_original or 'Desconocido'}\n"
            f"Género principal: {self.genero or 'Desconocido'}\n"
            f"Subgéneros: {', '.join(self.sub_generos) if self.sub_generos else 'Ninguno'}\n"
            f"Temporadas: {self.cantidad_temporadas or 'Desconocido'}\n"
            f"Episodios totales: {self.cantidad_episodios_totales or 'Desconocido'}\n"
            f"Ver en: {', '.join(self.donde_ver) if self.donde_ver else 'No disponible'}\n"
            f"Link: {self.link}"
        )
