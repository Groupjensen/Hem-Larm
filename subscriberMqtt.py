import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient
import os
from ledModule import control_led
from buzzerModule import start_buzzer, stop_buzzer, deinit_buzzer
from globals import system_mode, manual_commands  # Import shared variables

# Generate a random number for the MQTT client ID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = 'client_' + str(random_num)

# Adafruit IO configurations
ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'kabamaky'
ADAFRUIT_IO_KEY = 'XXXXXXXX'  # **Replace with your actual key**

# MQTT feed names
mqtt_led1 = 'kabamaky/feeds/led1'
mqtt_buzzer1 = 'kabamaky/feeds/buzzer1'
mqtt_alarm_control = 'kabamaky/feeds/alarmControl'
mqtt_mode_control = 'kabamaky/feeds/modeControl'  # New feed for mode control

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("SSID", "Password")  # **Replace with your Wi-Fi credentials**
    while not wlan.isconnected():
        print("Waiting for Wi-Fi connection...")
        time.sleep(1)
    print("Wi-Fi is connected")
    print(wlan.ifconfig())

# Function to connect to the MQTT broker
def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id,
                        server=ADAFRUIT_IO_URL,
                        user=ADAFRUIT_USERNAME,
                        password=ADAFRUIT_IO_KEY,
                        ssl=False)
    client.connect()
    print("Connected to Adafruit IO MQTT broker")
    return client

# Function to handle reconnection
def reconnect():
    print("Failed to connect to MQTT broker. Reconnecting...")
    time.sleep(5)
    machine.reset()

# Subscription callback
def sub_cb(topic, msg):
    global system_mode, manual_commands
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')
    print(f"Message received on topic: {topic} - Message: {msg}")

    if topic == mqtt_mode_control:
        if msg == "AUTO":
            system_mode = "AUTO"
            manual_commands.clear()  # Clear manual commands when switching to AUTO
            print("System mode set to AUTOMATIC")
        elif msg == "MANUAL":
            system_mode = "MANUAL"
            print("System mode set to MANUAL")
        elif msg == "DISABLE":
            system_mode = "DISABLE"
            print("System mode set to DISABLED")
            # Ensure devices are turned off
            control_led('OFF')
            stop_buzzer()
    elif system_mode == "MANUAL":
        # In MANUAL mode, control devices based on commands
        if topic == mqtt_led1:
            if msg == "ON":
                control_led("ON")
                time.sleep(5)
                print("Led1 is on")
            elif msg == "OFF":
                control_led("OFF")
                print("Led1 is off")
            
                
        
        elif topic == mqtt_buzzer1:
            manual_commands['BUZZER'] = msg
            if msg == "ON":
                start_buzzer(1000)
                time.sleep(5)
            elif msg == "OFF":
                stop_buzzer()
