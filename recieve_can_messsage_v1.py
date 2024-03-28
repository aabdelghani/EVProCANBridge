import can
import RPi.GPIO as GPIO

# Function to display a welcome message
def display_welcome():
    print("""
    Welcome to the CAN Message Listener and LED Toggle Script!
    -----------------------------------------------------------
    Author: Ahmed Abdelghany
    Email: ahmedabdelghany15@gmail.com

    Copyright (c) 2025 Vintage on Volt BV, Netherlands
    All rights reserved.
    
    This script listens for CAN messages on a specified interface.
    If a message with a predefined arbitration ID is received, it toggles the state of an LED.

    How it works:
    - Listens on the 'can1' interface for incoming CAN messages.
    - Checks each message for an arbitration ID of 0x123.
    - If a message with ID 0x123 is received, the script toggles an LED connected to GPIO 17.
      (If the LED is on, it turns off; if it's off, it turns on.)
    - Non-target messages (different IDs) are acknowledged but do not affect the LED.
    
    Press Ctrl+C to stop the script.
    """)

# Specify the CAN interface to listen on and the GPIO pin number
can_interface = 'can1'
led_pin = 17  # Adjust this pin number based on your hardware setup

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(led_pin, GPIO.OUT)  # Set the LED pin as output

def toggle_led():
    # Toggle the LED state and print the new state
    GPIO.output(led_pin, not GPIO.input(led_pin))
    print("LED state toggled.")

def receive_can_message():
    print(f"Listening for CAN messages on '{can_interface}'. Press Ctrl+C to exit.")
    with can.interface.Bus(channel=can_interface, bustype='socketcan') as bus:
        while True:
            message = bus.recv()  # Waits indefinitely for a message
            if message.arbitration_id == 0x123:
                print(f"Target message received: {message}")
                toggle_led()
            else:
                print(f"Non-target message received: ID 0x{message.arbitration_id:X}")

if __name__ == "__main__":
    display_welcome()  # Display the welcome screen
    try:
        receive_can_message()
    except KeyboardInterrupt:
        print("\nExecution terminated by user.")
    finally:
        GPIO.cleanup()  # Ensure a clean exit
        print("GPIO cleaned up. Goodbye!")
