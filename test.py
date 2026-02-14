"""
test.py
Prueba básica del sensor DHT22 (temperatura y humedad).
Basic DHT22 sensor test (temperature and humidity).
Author: Rodney Rojas
Sustainable MRI Lab
February 2026
Version: 1.0
"""
from dht_sensor import DHTSensor
import time

def main():
    sensor = DHTSensor()
    
    # temperature_c, humidity = sensor.read_sensor()
    # if temperature_c is not None:
    #     print(temperature_c, humidity)
        
        
    print(sensor.read_sensor())

if __name__ == "__main__":
    main()
