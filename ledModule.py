from machine import Pin

# Define the LED pin (change the pin number as required)
led_pin = 5  # Example: GPIO2

# Setup the LED pin
led = Pin(led_pin, Pin.OUT)
led.off()  # Ensure LED is off initially

# Function to control the LED
def control_led(state):
    if state == 'ON':
        led.on()
        print("LED is turned ON")
    elif state == 'OFF':
        led.off()
        print("LED is turned OFF")
    else:
        print("Invalid state! Use 'on' or 'off'.")
#control_led('OFF')