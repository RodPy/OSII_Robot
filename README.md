# OSII - ROBOT  

## Overview  

This project focuses on automating the acquisition and visualization of spatial data, primarily for MRI research applications. It combines robust hardware configurations with advanced software tools to enable efficient and precise data collection, visualization, and analysis.  

## Features  

- **Hardware Integration:** Includes CNC components and sensors for spatial measurements.  
- **Data Management:** Uses PostgreSQL for secure and efficient data handling.  
- **Visualization:** Generates 3D heatmaps and trajectory simulations using Matplotlib.  
- **Statistical Analysis:** Provides key metrics (maximum, minimum, mean, ppm) for advanced analysis.  
- **G-code Automation:** Automates CNC operations with spherical trajectory generation.  

## System Components  

### Hardware  

| **Component**                          | **Quantity** | **Price (USD)** | **Product Link**                                                                                                                                       |  
|-----------------------------------------|-------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|  
| Z Axis-300mm, XY-300mm-12mm Pitch       | 1           | 338.54           | [Link](https://www.aliexpress.us/item/3256805348651313.html?spm=a2g0o.order_detail.order_detail_item.3.5fa4f19cjVbIP4&gatewayAdapt=glo2usa)             |  
| Stepper Motor Driver TB6600             | 3           | 5.60             | [Link](https://www.aliexpress.us/item/3256805781393725.html?spm=a2g0o.order_detail.order_detail_item.2.1ed6f19cobQnNT&gatewayAdapt=glo2usa)             |  
| Raspberry Pi 3 Model B+                 | 1           | 30.00            | [Link](https://thepihut.com/products/raspberry-pi-3-model-b-plus)                                                                                      |  
| Official Raspberry Pi Touchscreen       | 1           | 50.00            | [Link](https://thepihut.com/products/official-raspberry-pi-7-touchscreen-display)                                                                      |  
| Temperature and Humidity Sensor DHT22   | 1           | 10.00            | [Link](https://thepihut.com/products/dht22-temperature-humidity-sensor)                                                                               |  
| Creality Ender-5 Plus 3D Printer        | 1           | 579.00           | [Link](https://www.creality.com/es/products/ender-5-plus-3d-printer)                                                                                   |  
| Arduino UNO R4 Minima                   | 1           | 16.00            | [Link](https://thepihut.com/products/arduino-uno-r4-minima)                                                                                            |  
| Gaussmeter Model GM2                    | 1           | 902.00           | [Link](https://www.alphalabinc.com/products/gm2/?srsltid=AfmBOor0p2l-VF9fIRODsZqY854WaDDNnBIFsOJ6kHjN2p6iCgCOzTLX)                                      |  
| **TOTAL**                               |             | **1940.34**      |                                                                                                                                                        |  

### Software  

| **Software** | **Description**                               | **Download Link**                        |  
|--------------|-----------------------------------------------|------------------------------------------|  
| OpenBuilds   | Platform for design, control, and simulation. | [Link](https://software.openbuilds.com/) |  

## Scripts Overview  

### `data_out.py`  

- Retrieves and visualizes 3D spatial data from PostgreSQL.  
- Generates heatmaps and calculates statistics (maximum, minimum, mean, ppm).  

### `database.py`  

- Manages interactions with PostgreSQL: table creation, record insertion, data retrieval, and deletion.  

### `main.py`  

- Used to measure the magnetic field of the OSII MRI.  
- Interacts with CNC machines via serial communication and logs Gaussmeter sensor data.  

### `serialCNC.py`  

- Facilitates serial communication with CNC devices.  
- Sends G-code commands and processes responses.  

### `sphere_path_generator.py`  

- Generates G-code for spherical trajectories.  
- Visualizes cutting paths and estimates execution time.  

### `visual_db_test.py`  

- Provides real-time 3D visualization of coordinates stored in the database.  

### `GaussmeterReader`  

- Used to measure the magnetic field of the OSII MRI through serial communication with a Gaussmeter sensor.  

## Installation and Setup  

1. Clone the repository:  
    ```bash  
    git clone https://github.com/RodPy/OSII_Robot  
    ```  
2. Install dependencies:  
    ```bash  
    pip install -r requirements.txt  
    ```  
3. Configure and populate your PostgreSQL database.  
4. Connect the hardware as described in the components section.  
5. Run the scripts for data collection, visualization, and analysis.  

## Contribution  

Contributions are welcome! Follow these steps:  
1. Fork the repository.  
2. Create a branch for your feature or bug fix.  
3. Commit your changes and open a pull request.  

## License  

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for more details.  

---  

**Version**: November 2024 - v6.1  
**Sustainable MRI Lab**  
