from subscriberMqtt import connect_to_wifi, mqtt_connect, reconnect
from subscriberMqtt import sub_cb, mqtt_led1, mqtt_buzzer1, mqtt_alarm_control, mqtt_mode_control
from sroSensor import DistanceSensor
from buzzerModule import start_buzzer, stop_buzzer, deinit_buzzer
from ledModule import control_led
from globals import system_mode, manual_commands  # Import shared variables
import time

# Constants
ALARM_THRESHOLD = 7  # Distance in cm

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
connect_to_wifi()

# Connect to MQTT broker
print("Connecting to MQTT broker...")
try:
    client = mqtt_connect()
except OSError as e:
    # Handle reconnection logic if needed
    reconnect()

# Set the callback for the subscription
client.set_callback(sub_cb)

# Subscribe to the topics
print("Subscribing to topics...")
client.subscribe(mqtt_led1)
client.subscribe(mqtt_buzzer1)
client.subscribe(mqtt_alarm_control)
client.subscribe(mqtt_mode_control)  # Subscribe to mode control topic

# Initialize Distance Sensor
trigger_pin = 27
echo_pin = 26
sensor = DistanceSensor(trigger_pin, echo_pin)

try:
    while True:
        # Check for messages (non-blocking)
        client.check_msg()

        if system_mode == "AUTO":
            print("Measuring distance in AUTO mode...")
            distance = sensor.measure_distance()
            print(f"The distance from the object is {distance:.2f} cm")

            # Publish distance data
            client.publish('kabamaky/feeds/sroSensor', f'{distance:.2f} cm', qos=0)

            if distance > ALARM_THRESHOLD:
                # Publish alarm status
                client.publish('kabamaky/feeds/alarmStatus', '1', qos=0)
                print("Distance exceeded threshold! Triggering alarm.")
                # Turn on LED and buzzer
                control_led('ON')
                start_buzzer(1000)
            else:
                # Publish alarm status
                client.publish('kabamaky/feeds/alarmStatus', '0', qos=0)
                # Turn off LED and buzzer
                control_led('OFF')
                stop_buzzer()

        elif system_mode == "MANUAL":
            # In MANUAL mode, devices are controlled via MQTT messages in sub_cb
            print("System is in MANUAL mode. Waiting for manual commands...")
            # Devices are already controlled in sub_cb, so no action needed here

        elif system_mode == "DISABLE":
            # In DISABLE mode, ensure devices are off
            print("System is DISABLED. Alarm and devices are off.")
            control_led('OFF')
            stop_buzzer()
            # Optionally publish alarm status as disabled
            client.publish('kabamaky/feeds/alarmStatus', 'Disabled', qos=0)

        time.sleep(8)
except KeyboardInterrupt:
    # Clean up on exit
    stop_buzzer()
    deinit_buzzer()
    control_led('OFF')
    client.disconnect()
    print("Script interrupted and exiting")
