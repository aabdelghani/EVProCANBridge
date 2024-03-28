import can
import RPi.GPIO as GPIO
import time

# Specify the CAN interface to listen on
can_interface = 'can1'

# GPIO pin to use for the LED (using BCM numbering)
led_pin = 17  # Change to your actual pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(led_pin, GPIO.OUT)  # Set the LED pin as output

def receive_can_message():
    with can.interface.Bus(channel=can_interface, bustype='socketcan') as bus:
        print("Listening for CAN messages on", can_interface)
        while True:
            # Block and wait for an incoming message
            message = bus.recv()  # Timeout can be added as an argument (in seconds)
            if message:
                # Check if the received message has the specific arbitration ID
                if message.arbitration_id == 0x123:  # The ID you're looking for
                    print(f"Received target message: {message}")
                    # Turn on the LED
                    GPIO.output(led_pin, GPIO.HIGH)
                    print("LED turned ON")
                    break  # Exit the loop after receiving the target message

if __name__ == "__main__":
    try:
        receive_can_message()
    except KeyboardInterrupt:
        print("\nScript terminated by user")
    finally:
        # Cleanup GPIO (turn off LED and set pin to input to ensure a clean state)
        GPIO.output(led_pin, GPIO.LOW)
        GPIO.cleanup()
        print("GPIO cleaned up")
