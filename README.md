# OSII Robot

Sistema de escaneo esférico para mapeo de campo magnético mediante control CNC, gaussmeter y registro en base de datos.

Spherical scanning system for magnetic field mapping using CNC control, gaussmeter and database logging.

---

## Descripción / Description

**Español:** Este proyecto controla un robot CNC para realizar escaneos esféricos de un volumen, leyendo intensidad de campo magnético (gaussmeter) en cada punto. Los datos se almacenan en PostgreSQL junto con temperatura y humedad (sensor DHT22). Incluye interfaces gráficas y herramientas de visualización.

**English:** This project controls a CNC robot to perform spherical scans of a volume, reading magnetic field strength (gaussmeter) at each point. Data is stored in PostgreSQL along with temperature and humidity (DHT22 sensor). It includes graphical interfaces and visualization tools.

---

## Requisitos / Requirements

- Python 3.8+
- PostgreSQL
- Raspberry Pi (rama `raspberrypi3`) o PC con puertos seriales
- Hardware: CNC (Grbl), gaussmeter, sensor DHT22

---

## Instalación / Installation

### 1. Clonar el repositorio

```bash
git clone https://github.com/RodPy/OSII_Robot.git
cd OSII_Robot
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / Raspberry Pi:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Crear base de datos y usuario. Por defecto el proyecto usa:
- Usuario: `postgres`
- Contraseña: `admin`
- Host: `localhost`

Ajustar en `main.py` y `database.py` según tu configuración.

---

## Estructura del proyecto / Project Structure

```
OSII_Robot/
├── main.py                 # Aplicación principal / Main application
├── database.py             # Módulo PostgreSQL
├── dht_sensor.py           # Sensor temperatura/humedad (Raspberry Pi)
├── gaussmeter_reader.py    # Lectura del gaussmeter
├── serialCNC.py            # Comunicación serial con CNC
├── sphere_path_generator.py # Generación de trayectoria esférica
├── calibrate_robot.py      # Modo calibración (eje Y)
├── heatmap_visualization.py # Visualización mapa de calor (static/gif/csv)
├── visual_bd_test.py       # Gráfico 3D en tiempo real
├── robot_gui.py            # GUI Simulador (Tkinter)
├── view.py                 # GUI Control Robot CNC (Tkinter)
├── test.py                 # Prueba sensor DHT22
├── requirements.txt
└── README.md
```

---

## Uso / Usage

### Aplicación principal

```bash
python main.py
```

Configurar en `main.py`:
- `bd`: nombre de la base de datos
- `puerto_serial`: `/dev/ttyACM0` (Linux/Raspberry) o `COMx` (Windows)
- `radius`, `step`, `speed`, `sample_time`: parámetros del escaneo

### Calibración

```bash
python calibrate_robot.py
```

### Visualización de datos

```bash
# Gráfico estático
python heatmap_visualization.py --mode static --db NOMBRE_BD

# Exportar a CSV
python heatmap_visualization.py --mode csv --db NOMBRE_BD --output datos.csv

# Generar GIF animado
python heatmap_visualization.py --mode gif --db NOMBRE_BD
```

### Interfaces gráficas

```bash
# Simulador (conexión, movimiento, visualización en vivo)
python robot_gui.py

# Control Robot CNC (puertos seriales, configuración)
python view.py

# Gráfico 3D en tiempo real desde BD
python visual_bd_test.py
```

### Prueba de sensores

```bash
python test.py   # Prueba DHT22
```

---

## Puertos seriales / Serial Ports

| Dispositivo | Linux / Raspberry Pi | Windows |
|-------------|----------------------|---------|
| CNC (Grbl)  | `/dev/ttyACM0`       | `COM3`  |
| Gaussmeter  | `/dev/ttyUSB0`       | `COMx`  |

Verificar puertos disponibles:
- **Linux:** `ls /dev/tty*`
- **Windows:** Administrador de dispositivos → Puertos (COM y LPT)

---

## Ramas / Branches

- `main` - Versión principal
- `raspberry` - Adaptada para Raspberry Pi
- `raspberrypi3` - Versión específica Raspberry Pi 3

---

## Autor / Author

**Rodney Rojas**  
Sustainable MRI Lab  
February 2026 · Version 1.0
