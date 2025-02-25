from umqtt.simple import MQTTClient
import time
import machine
import os
from funcConnect import connect

# Connect to WiFi
connect()

# Generate a random number from 3 random bytes and convert it to an integer
random_num = int.from_bytes(os.urandom(3), 'little')

# Create a unique MQTT client ID using the random number
mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

# Adafruit IO configurations
ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'kabamaky'
ADAFRUIT_IO_KEY = 'XXXXXX' #Replace with your keys

mqtt_sroSensor = 'kabamaky/feeds/sroSensor'
mqtt_led1 = 'kabamaky/feeds/led1'
mqtt_buzzer1 = 'kabamaky/feeds/buzzer1'

mqtt_mode_control ='/kabamaky/feeds/modecontrol'

# Define the function to connect to the MQTT broker
def sure_mqtt_connection():
    
    def mqtt_connect():
        client = MQTTClient(client_id=mqtt_client_id,
                            server=ADAFRUIT_IO_URL,
                            user=ADAFRUIT_USERNAME,
                            password=ADAFRUIT_IO_KEY, ssl=False)
        
        client.connect()
        print("Connected to Adafruit IO MQTT broker")
        return client

    def reconnect():
        print("Failed to connect to the MQTT broker, reconnecting...")
        time.sleep(2)
        machine.reset()
    
    try:
        client = mqtt_connect()
        return client
    
    except OSError as e:
        reconnect()
