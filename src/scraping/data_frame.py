"""Funciones para manipular y guardar DataFrames de series de TV."""

import pickle

import pandas as pd
from datos_serie import DatosSerie, SerieColumn, SerieNullValues


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
        null_value = SerieNullValues[field.upper()].value
        if field in (
            SerieColumn.TITULO.value,
            SerieColumn.TITULO_ORIGINAL.value,
        ):
            df[field] = df[field].fillna(null_value).astype(str).str.strip()
        elif field in (SerieColumn.GENEROS.value, SerieColumn.DONDE_VER.value):
            # Normaliza listas representadas como string
            df[field] = (
                df[field]
                .fillna("")
                .apply(
                    lambda x: (
                        x if isinstance(x, str) else ", ".join(x) if isinstance(x, list) else str(x)
                    )
                )
            )
            df[field] = df[field].replace({"": null_value, None: null_value})
        elif field in (
            SerieColumn.FECHA_EMISION_ORIGINAL.value,
            SerieColumn.FECHA_EMISION_ULTIMA.value,
        ):
            df[field] = pd.to_numeric(df[field], errors="coerce").fillna(null_value).astype(int)
        elif field in (
            SerieColumn.CANTIDAD_TEMPORADAS.value,
            SerieColumn.CANTIDAD_EPISODIOS_TOTALES.value,
        ):
            df[field] = pd.to_numeric(df[field], errors="coerce").fillna(null_value).astype(int)
        elif field == SerieColumn.PUNTUACION.value:
            df[field] = pd.to_numeric(df[field], errors="coerce").fillna(null_value)
        elif field == SerieColumn.LINK.value:
            df[field] = df[field].fillna(null_value).astype(str).str.strip()
    return df


def guardar_dataframe_pickle(df: pd.DataFrame, filename: str):
    """Guarda el DataFrame en un archivo pickle."""
    with open(filename, "wb") as f:
        pickle.dump(df, f)
