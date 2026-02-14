"""
October 2024 - Version 2.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

database.py
Proporciona operaciones con PostgreSQL: crear tabla, insertar datos (simple o por lotes),
consultar y eliminar. Soporta uso como context manager.
"""
from __future__ import annotations

import psycopg2
from typing import Any, List, Optional, Tuple
from contextlib import contextmanager


class Database:
    """Conexión y operaciones sobre la tabla 'data' (coordenadas 3D y sonda)."""

    TABLE_NAME = "data"
    INSERT_COLUMNS = (
        "date", "coordinate_x", "coordinate_y", "coordinate_z",
        "y_probe", "sample_time", "sample_distance"
    )
    INSERT_PLACEHOLDERS = ", ".join(["%s"] * 7)

    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cur = self.conn.cursor()

    def create_table(self) -> None:
        """Crea la tabla 'data' si no existe."""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id SERIAL PRIMARY KEY,
                date DATE,
                coordinate_x FLOAT,
                coordinate_y FLOAT,
                coordinate_z FLOAT,
                y_probe FLOAT,
                sample_time TIMESTAMP,
                sample_distance FLOAT
            )
        """)
        self.conn.commit()

    def insert_data(
        self,
        date: Any,
        coordinate_x: float,
        coordinate_y: float,
        coordinate_z: float,
        y_probe: float,
        sample_time: Any,
        sample_distance: float,
        commit: bool = True,
    ) -> None:
        """Inserta un registro. Si commit=False, se puede hacer commit en lote después."""
        self.cur.execute(
            f"""
            INSERT INTO {self.TABLE_NAME}
            ({", ".join(self.INSERT_COLUMNS)})
            VALUES ({self.INSERT_PLACEHOLDERS})
            """,
            (date, coordinate_x, coordinate_y, coordinate_z, y_probe, sample_time, sample_distance),
        )
        if commit:
            self.conn.commit()

    def insert_many(self, rows: List[Tuple[Any, ...]]) -> None:
        """Inserta múltiples registros en una sola transacción."""
        if not rows:
            return
        self.cur.executemany(
            f"""
            INSERT INTO {self.TABLE_NAME}
            ({", ".join(self.INSERT_COLUMNS)})
            VALUES ({self.INSERT_PLACEHOLDERS})
            """,
            rows,
        )
        self.conn.commit()

    def select_all_data(self) -> List[Tuple[Any, ...]]:
        """Devuelve todos los registros de la tabla."""
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME}")
        return self.cur.fetchall()

    def delete_data(self, record_id: int) -> None:
        """Elimina un registro por id."""
        self.cur.execute(f"DELETE FROM {self.TABLE_NAME} WHERE id = %s", (record_id,))
        self.conn.commit()

    def commit(self) -> None:
        """Fuerza commit de la transacción actual."""
        self.conn.commit()

    def close(self) -> None:
        """Cierra cursor y conexión."""
        if self.cur:
            try:
                self.cur.close()
            except Exception:
                pass
            self.cur = None
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


@contextmanager
def database_connection(dbname: str, user: str, password: str, **kwargs: Any):
    """Context manager para usar la base de datos y cerrar al salir."""
    db = Database(dbname=dbname, user=user, password=password, **kwargs)
    try:
        yield db
    finally:
        db.close()
