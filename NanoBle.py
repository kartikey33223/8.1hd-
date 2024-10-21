from bluepy import btle
import time
from gpiozero import PWMLED
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BOARD)

# Initialize LED at GPIO pin 18
blue_led = PWMLED(18)

def map_lux_to_analog_value(lux, max_lux=1500):
    # Map lux (0 to max_lux) to (0 to 255)
    analog_value = int((lux / max_lux) * 255)
    
    # Ensure the value is between 0 and 255
    analog_value = max(0, min(255, analog_value))
    
    return analog_value
    
def connect_and_read_ble(device_mac, characteristic_uuid):
    try:
        # Connect to the BLE device
        print(f"Connecting to {device_mac}...")
        device = btle.Peripheral(device_mac, btle.ADDR_TYPE_PUBLIC)

        # Get the characteristic by UUID and read its value
        print(f"Reading characteristic {characteristic_uuid}...")
        
        while(True):
            characteristic = device.getCharacteristics(uuid=characteristic_uuid)[0]
            value = characteristic.read()
            number = int.from_bytes(value, byteorder='big')  # Convert to integer
            print(f"Value: {number}")
            
            # Mapping the value of lux into analog value
            analog_value = map_lux_to_analog_value(number, 150)
            print(f"Analog Value: {analog_value}")
            blue_led.value = 1 - (analog_value / 255)
            
    except Exception as e:
        print(f"Failed to connect or read from {device_mac}: {str(e)}")
        device.disconnect()
        print("Disconnected")
    except KeyboardInterrupt:
        # Always disconnect after finishing
        print("Disconnecting...")
        device.disconnect()
        print("Disconnected")


if __name__ == "__main__":
    # BLE device's MAC address and characteristic UUID
    device_mac_address = "D3:72:9F:4C:11:67"  
    characteristic_uuid = "2A6E"  

    connect_and_read_ble(device_mac_address, characteristic_uuid)
