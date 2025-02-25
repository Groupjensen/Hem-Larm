import network 
import time

def connect():
    wlan = network.WLAN(network.STA_IF)  # Initialize Wi-Fi station interface
    wlan.active(True)  # Activate the Wi-Fi interface
    
    # Retry connecting to Wi-Fi
    while not wlan.isconnected():
        try:
            wlan.connect("SSId", "Password")  # Connect to Wi-Fi network Change to own password and user
            print("Attempting to connect...")
            
            # Wait until the Wi-Fi is connected
            timeout = 0
            while not wlan.isconnected() and timeout < 10:
                time.sleep(1)  # Wait for 1 second before checking again
                timeout += 1
            
            if wlan.isconnected():
                break  # Exit the loop if connected
                
        except OSError as e:
            print("Wi-Fi connection failed, retrying...", e)
            wlan.active(False)  # Deactivate the Wi-Fi interface
            time.sleep(2)
            wlan.active(True)  # Reactivate the Wi-Fi interface
    
    if wlan.isconnected():
        print("Wi-Fi is connected...")  # Print success message
        print(wlan.ifconfig())  # Print network configuration
    else:
        print("Failed to connect to Wi-Fi after multiple attempts")




