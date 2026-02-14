"""
October 2024 - Version 3.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

visual_bd_test.py
Visualización 3D en tiempo (casi) real de coordenadas leídas desde PostgreSQL.
Actualiza el gráfico cada segundo. Ctrl+C para salir.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database import Database


def main() -> None:
    db = Database(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    cursor = db.conn.cursor()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")

    try:
        plt.ion()
        plt.show()
        while True:
            cursor.execute(
                "SELECT coordinate_x, coordinate_y, coordinate_z FROM data"
            )
            rows = cursor.fetchall()
            if rows:
                xs, ys, zs = zip(*rows)
                ax.clear()
                ax.set_xlabel("X Coordinate")
                ax.set_ylabel("Y Coordinate")
                ax.set_zlabel("Z Coordinate")
                ax.scatter(xs, ys, zs, c="g", marker="o")
                plt.draw()
            plt.pause(1)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        db.close()


if __name__ == "__main__":
    main()
