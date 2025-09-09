import glob
import os
import pickle

import pandas as pd
from const import settings


def main():
    # Buscar todos los archivos que coincidan con el patrón 'series_tv_*.pkl' en el directorio principal
    directorio_principal = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    patron = os.path.join(directorio_principal, "series_tv_*_*.pkl")
    archivos = [f for f in glob.glob(patron) if os.path.basename(f) != settings.nombre_archivo_pkl]

    if not archivos:
        print("No se encontraron archivos para fusionar.")
        exit(1)

    dfs = []
    for archivo in archivos:
        with open(archivo, "rb") as f:
            df = pickle.load(f)
            dfs.append(df)

    # Concatenar todos los DataFrames
    df_final = pd.concat(dfs, ignore_index=True)

    # Guardar el DataFrame fusionado
    archivo_salida = os.path.join(directorio_principal, settings.nombre_archivo_pkl)
    with open(archivo_salida, "wb") as f:
        pickle.dump(df_final, f)
    print(f"Datos fusionados guardados en {archivo_salida}. Total de series: {len(df_final)}")


if __name__ == "__main__":
    main()
