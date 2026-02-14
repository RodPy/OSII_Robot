"""
Configuración centralizada del proyecto OSII_Robot.
Usa variables de entorno cuando existan; si no, valores por defecto.
"""
import os

# Base de datos
DB_NAME: str = os.environ.get("OSII_DB_NAME", "Ossi_November_XX")
DB_USER: str = os.environ.get("OSII_DB_USER", "postgres")
DB_PASSWORD: str = os.environ.get("OSII_DB_PASSWORD", "admin")
DB_HOST: str = os.environ.get("OSII_DB_HOST", "localhost")
DB_PORT: int = int(os.environ.get("OSII_DB_PORT", "5432"))
# BD para scripts de exportación/visualización (data_out, visual_bd_test)
EXPORT_DB_NAME: str = os.environ.get(
    "OSII_EXPORT_DB",
    "Ossi_04_11_2024_Y_FULL_SHIM_D22_CENTER",
)

# Puertos serie
SERIAL_CNC_PORT: str = os.environ.get("OSII_CNC_PORT", "COM3")
SERIAL_GAUSSMETER_PORT: str = os.environ.get("OSII_GAUSSMETER_PORT", "COM4")
SERIAL_BAUD_RATE: int = int(os.environ.get("OSII_BAUD_RATE", "115200"))

# Parámetros de esfera y medición
SPHERE_RADIUS: int = int(os.environ.get("OSII_SPHERE_RADIUS", "120"))
SPHERE_STEP: int = int(os.environ.get("OSII_SPHERE_STEP", "10"))
SPHERE_SPEED: int = int(os.environ.get("OSII_SPHERE_SPEED", "450"))
SAMPLE_TIME_SEC: float = float(os.environ.get("OSII_SAMPLE_TIME", "2"))

# Serial timeouts (segundos)
GCODE_SEND_DELAY: float = 1.0
GAUSSMETER_READ_TIMEOUT: float = 2.0
GAUSSMETER_MAX_RETRIES: int = 100
