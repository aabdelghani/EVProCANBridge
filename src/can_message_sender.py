import can
import json

def display_welcome():
    print("""
    Welcome to the CAN Message Sending Script!
    ------------------------------------------
    Author: Ahmed Abdelghany
    Email: ahmedabdelghany15@gmail.com

    Copyright (c) 2025 Vintage on Volt BV, Netherlands
    All rights reserved.
    
    This script sends a specific CAN message over the CAN bus using a designated interface.

    How it works:
    - Reads configuration from 'config.json'.
    - Utilizes a specified interface for sending messages.
    - Constructs a CAN message with a predefined arbitration ID and data payload.
    - Attempts to send the message over the CAN bus.
    - Notifies the user whether the message was successfully sent or if an error occurred.

    Usage:
    Simply run the script. Ensure that 'config.json' exists and is properly configured.
    The script will automatically attempt to send the predefined CAN message and report on its success or failure.
    Please ensure that the 'python-can' library is installed and that the necessary CAN interface is properly configured on your system.
    Press Ctrl+C to exit the script if it's running in a loop or wait for the script to complete its execution.
    """)

def load_config():
    # Adjust the path to match the new directory structure
    config_path = '../config/can_sender_config.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def send_can_message(config):
    can_interface = config["can_interface"]
    arbitration_id = config["arbitration_id"]
    data_payload = config["data_payload"]
    is_extended_id = config["is_extended_id"]
    
    with can.interface.Bus(channel=can_interface, bustype='socketcan') as bus:
        message = can.Message(arbitration_id=arbitration_id, data=data_payload, is_extended_id=is_extended_id)
        
        try:
            bus.send(message)
            print("Message sent on {}: {}".format(can_interface, message))
        except can.CanError:
            print("Message failed to send")

if __name__ == "__main__":
    display_welcome()
    config = load_config()
    send_can_message(config)
