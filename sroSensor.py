import time
from machine import Pin

class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin, max_distance=400):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.max_distance = max_distance
        self.trigger.value(0)

    def measure_distance(self):
        # Send trigger pulse
        self.trigger.value(0)
        time.sleep_us(2)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        # Wait for echo pulse
        signaloff, signalon = 0, 0

        while self.echo.value() == 0:
            signaloff = time.ticks_us()

        while self.echo.value() == 1:
            signalon = time.ticks_us()

        # Calculate distance
        duration = signalon - signaloff
        distance = (duration / 2) / 29.1  # Convert duration to distance in cm (speed of sound 34300 cm/s)

        # Cap the distance to the max distance
        if distance > self.max_distance:
            distance = self.max_distance

        return distance
