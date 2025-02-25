import time
from machine import Pin, PWM

# Define the buzzer pin
buzzer_pin = 15  # Change this to your GPIO pin

# Setup PWM on the buzzer pin
buzzer = PWM(Pin(buzzer_pin, Pin.OUT))
buzzer.duty_u16(0)  # Ensure buzzer is off initially

# Function to play a tone
def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)  # 50% duty cycle (32768 is half of 65536)
    time.sleep_ms(duration)
    buzzer.duty_u16(0)  # Turn off the buzzer
    
def start_buzzer(frequency):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)  # 50% duty cycle to produce sound
    
# Function to stop the buzzer
def stop_buzzer():
    buzzer.duty_u16(0)  # Set duty cycle to 0 to stop sound
    
# Function to deinitialize the buzzer
def deinit_buzzer():
    buzzer.deinit()

# Example usage
#play_tone(1000, 500)
