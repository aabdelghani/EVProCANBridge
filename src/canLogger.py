import can
import json
import os
import subprocess
from can.listener import Listener
import csv

# Define full paths for configuration and log files
CONFIG_FILE_PATH = "/home/vov003/Desktop/EVProCANBridge/config/canLogger.json"
LOG_DIRECTORY_PATH = "/home/vov003/Desktop/EVProCANBridge/log"

class CustomCSVWriter(Listener):
    def __init__(self, filename):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Open the file with line buffering
        self.file = open(filename, mode='a', newline='', buffering=1)
        self.writer = csv.writer(self.file)
        # Write header if the file is new/empty
        if os.path.getsize(filename) == 0:
            self.writer.writerow(['timestamp', 'arbitration_id', 'extended', 'remote', 'error', 'dlc', 'data'])

    def on_message_received(self, msg):
        # Prepare the message data
        message_data = [
            msg.timestamp,
            hex(msg.arbitration_id),
            msg.is_extended_id,
            msg.is_remote_frame,
            msg.is_error_frame,
            msg.dlc,
            msg.data.hex()
        ]
        # Write the message data to the CSV file
        self.writer.writerow(message_data)
        # Flush the file to ensure the data is written immediately
        self.file.flush()

    def stop(self):
        self.file.close()

def configure_can_interface(interface):
    # Command templates for setting up the CAN interface
    setup_commands = [
        f"sudo ip link set {interface} up type can bitrate 500000",
        f"sudo ifconfig {interface} txqueuelen 65536",
    ]
    
    for command in setup_commands:
        subprocess.run(command.split(), check=True)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Configuration file not found, using default settings.")
        return {"default_can_interface": "can0"}

def setup_logging(bus):
    log_directory = LOG_DIRECTORY_PATH
    filename = os.path.join(log_directory, 'can_messages.csv')
    custom_writer = CustomCSVWriter(filename)
    notifier = can.Notifier(bus, [custom_writer])
    return notifier, filename, custom_writer.stop

def main():
    config = load_config()
    user_can_interface = config.get("default_can_interface", "can0")

    bus = can.interface.Bus(bustype='socketcan', channel=user_can_interface, bitrate=500000)
    
    notifier, log_file_path, cleanup_func = setup_logging(bus)
    
    print("Logging CAN messages. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping logging...")
    finally:
        notifier.stop()
        print(f"Log files saved in {log_file_path}")
        cleanup_func()

if __name__ == '__main__':
    main()
