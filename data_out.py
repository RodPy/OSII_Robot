"""
November 2024 - Version 5.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

data_out.py
Exporta datos 3D desde PostgreSQL a CSV y genera un heatmap 3D (scatter) con estadísticas
(max, min, media, ppm). Ejecutar como script: python data_out.py
"""
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    EXPORT_DB_NAME,
)
from database import Database

PPM_CENTER_REF = 436


def load_data(db: Database) -> pd.DataFrame:
    """Carga coordenadas y sonda desde la tabla 'data'."""
    query = """
        SELECT date, coordinate_x, coordinate_y, coordinate_z,
               y_probe, sample_time, sample_distance
        FROM data
    """
    return pd.read_sql_query(query, db.conn)


def export_csv(df: pd.DataFrame, base_name: str) -> str:
    """Guarda el DataFrame en CSV y devuelve la ruta del archivo."""
    path = f"{base_name}.csv"
    df.to_csv(path, index=False)
    return path


def plot_heatmap_3d(df: pd.DataFrame) -> None:
    """Genera scatter 3D con color por y_probe y muestra estadísticas."""
    if df.empty or "y_probe" not in df.columns:
        print("No hay datos para graficar.")
        return

    x = df["coordinate_x"].to_numpy()
    y = df["coordinate_y"].to_numpy()
    z = df["coordinate_z"].to_numpy()
    c = df["y_probe"].to_numpy()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    scatter = ax.scatter(x, y, z, c=c, cmap="hot")
    fig.colorbar(scatter, label="Y Probe")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")
    ax.set_title("3D Heatmap of Y_PROBE")
    plt.show()


def print_stats(df: pd.DataFrame) -> None:
    """Imprime max, min, media y PPM de y_probe."""
    if df.empty or "y_probe" not in df.columns:
        return
    max_val = df["y_probe"].max()
    min_val = df["y_probe"].min()
    mean_val = df["y_probe"].mean()
    if mean_val != 0:
        ppm = ((max_val - min_val) / mean_val) * 1_000_000
    else:
        ppm = float("nan")
    print(
        f"Max: {max_val:.2f} - Min: {min_val:.2f} - Mean: {mean_val:.2f} "
        f"- Center: {PPM_CENTER_REF} - PPM: {ppm:.2f}"
    )


def main() -> None:
    db = Database(
        dbname=EXPORT_DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    try:
        df = load_data(db)
        path = export_csv(df, EXPORT_DB_NAME)
        print(f"Data exported to {path}")
        print_stats(df)
        plot_heatmap_3d(df)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
