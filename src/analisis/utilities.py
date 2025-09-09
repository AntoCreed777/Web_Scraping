import os
import sys
from typing import Optional

import pandas as pd

# Para poder importar de src.scraping
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scraping.const import settings


def importar_data_frame() -> pd.DataFrame:
    return pd.read_pickle(settings.nombre_archivo_pkl)


def imprimir_data_frame(
    df: pd.DataFrame,
    mensaje: str,
    columnas: Optional[list[str]] = None,
    cantidad: Optional[int] = None,
):
    """
    Imprime el DataFrame en formato tabla markdown.
    Si se especifica una lista de columnas, solo muestra esas columnas.
    """
    if columnas is not None:
        df = df[columnas]

    print(f"\n{mensaje}")

    if df.empty:
        print("El DataFrame está vacío.")
        return

    if cantidad is None:
        print(df.to_markdown(index=False))
        print(f"Filas mostradas: {len(df)}")
    else:
        print(df.head(cantidad).to_markdown(index=False))


def split_df(df: pd.DataFrame, columna: str) -> tuple[str, pd.DataFrame]:
    COLUMNA_SPLIT = columna + "_split"

    # Separar en listas
    df[COLUMNA_SPLIT] = df[columna].str.split(",")

    # Explode para tener una fila por cada elemento
    df_exploded = df.explode(COLUMNA_SPLIT)

    # Limpiar espacios extra
    df_exploded[COLUMNA_SPLIT] = df_exploded[COLUMNA_SPLIT].str.strip()

    return COLUMNA_SPLIT, df_exploded
