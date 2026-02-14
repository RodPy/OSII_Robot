"""
heatmap_visualization.py
Visualización de mapa de calor 3D desde PostgreSQL. Modos: static, gif, csv.
3D heatmap visualization from PostgreSQL. Modes: static, gif, csv.
Usage: python heatmap_visualization.py [--mode static|gif|csv] [--db DB_NAME]
Author: Rodney Rojas
Sustainable MRI Lab
February 2026
Version: 1.0
"""
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from database import Database


def load_data(dbname, user='postgres', password='admin'):
    """Carga datos de coordenadas y sonda desde PostgreSQL."""
    db = Database(dbname=dbname, user=user, password=password)
    query = "SELECT date, temperature_c, humidity, coordinate_x, coordinate_y, coordinate_z, y_probe FROM data"
    df = pd.read_sql_query(query, db.conn)
    db.close()
    return df


def plot_static_heatmap(df, title='Mapa de Calor 3D - y_probe'):
    """Genera y muestra gráfico 3D estático."""
    x = df['coordinate_y'].to_numpy()
    y = df['coordinate_x'].to_numpy()
    z = df['coordinate_z'].to_numpy()
    c = df['y_probe'].to_numpy()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=c, cmap='hot')
    fig.colorbar(scatter, label='y_probe')
    ax.set_xlabel('coordinate_y')
    ax.set_ylabel('coordinate_x')
    ax.set_zlabel('coordinate_z')
    ax.set_title(title)
    plt.show()


def export_csv(df, output_file):
    """Exporta datos a CSV."""
    df.to_csv(output_file, index=False)
    print(f"Datos exportados a {output_file}")


def create_gif_heatmap(df, output_file='heatmap_3d.gif', fps=10):
    """Genera GIF animado del mapa de calor 3D."""
    import imageio

    x = df['coordinate_y'].to_numpy()
    y = df['coordinate_x'].to_numpy()
    z = df['coordinate_z'].to_numpy()
    c = df['y_probe'].to_numpy()

    frames = []
    temp_files = []

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for angle in range(0, 360, 10):
        ax.clear()
        ax.scatter(x, y, z, c=c, cmap='hot')
        ax.view_init(30, angle)
        ax.set_xlabel('coordinate_x')
        ax.set_ylabel('coordinate_y')
        ax.set_zlabel('coordinate_z')
        ax.set_title('Mapa de Calor 3D')

        filename = f'frame_{angle}.png'
        plt.savefig(filename)
        temp_files.append(filename)
        frames.append(imageio.imread(filename))

    plt.close()
    imageio.mimsave(output_file, frames, fps=fps)

    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

    print(f"GIF guardado en {output_file}")


def print_stats(df):
    """Imprime estadísticas del campo y_probe."""
    probe = df['y_probe']
    print(f"Max: {probe.max()} - Min: {probe.min()} - Prom: {probe.mean()}")


def main():
    parser = argparse.ArgumentParser(description='Visualización mapa de calor 3D')
    parser.add_argument('--mode', choices=['static', 'gif', 'csv'], default='static',
                        help='Modo: static (gráfico), gif (animación), csv (exportar)')
    parser.add_argument('--db', default='Ossi_24_11_2024_Y_FULL_SHIM_D25_CENTER',
                        help='Nombre de la base de datos')
    parser.add_argument('--output', default=None, help='Archivo de salida (CSV o GIF)')
    args = parser.parse_args()

    df = load_data(args.db)
    print_stats(df)

    if args.mode == 'static':
        plot_static_heatmap(df)
    elif args.mode == 'csv':
        output = args.output or f'{args.db}.csv'
        export_csv(df, output)
    elif args.mode == 'gif':
        output = args.output or 'heatmap_3d.gif'
        create_gif_heatmap(df, output)


if __name__ == "__main__":
    main()
