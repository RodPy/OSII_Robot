"""
dht_sensor.py
Lectura del sensor DHT22 para temperatura y humedad (Raspberry Pi).
DHT22 sensor reading for temperature and humidity (Raspberry Pi).
Author: Rodney Rojas
Sustainable MRI Lab
February 2026
Version: 1.0
"""
import time
import board
import adafruit_dht
import time 

class DHTSensor:
    def __init__(self, pin=board.D21):
        self.dhtDevice = adafruit_dht.DHT22(pin)
    
    def read_sensor(self):
        try:
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity
            time.sleep(2)
            return temperature_c, humidity
        
        except RuntimeError as error:
            print(f"RuntimeError: {error.args[0]}")
            return None, None
        
        except Exception as error:
            self.dhtDevice.exit()
            raise error
    
    def close(self):
        self.dhtDevice.exit()
