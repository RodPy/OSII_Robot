# main.py

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
