"""Funciones para manipular y guardar DataFrames de series de TV."""

import pickle

import pandas as pd
from datos_serie import DatosSerie


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
