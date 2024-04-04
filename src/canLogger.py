import can
import json
import os

def load_config():
    try:
        with open('../config/canLogger.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {"default_format": "csv", "default_can_interface": "can0"}

def setup_logging(bus, log_format):
    # Define all formats we want to log in
    log_formats = ['asc', 'db', 'csv', 'log', 'trc']  # Extendable for more formats
    log_directory = "../log"

    # Ensure the log directory exists
    os.makedirs(log_directory, exist_ok=True)

    if log_format not in log_formats:
        print(f"Unsupported format '{log_format}'. Falling back to CSV.")
        log_format = 'csv'
    
    filename = os.path.join(log_directory, f'can_messages.{log_format}')
    if log_format == 'asc':
        listener = can.ASCWriter(filename)
    elif log_format == 'db':
        listener = can.SqliteWriter(filename)
    elif log_format == 'csv':
        listener = can.CSVWriter(filename)
    elif log_format == 'log':
        listener = can.CanutilsLogWriter(filename)
    elif log_format == 'trc':
        listener = can.TRCWriter(filename)
    
    # Attach the listener to a notifier
    notifier = can.Notifier(bus, [listener])
    
    return notifier, filename

def main():
    config = load_config()
    default_format = config.get("default_format", "csv")
    default_can_interface = config.get("default_can_interface", "can0")
    
    # Ask the user for their preferred log format and CAN interface
    user_format = input(f"Enter the desired log format [{default_format}]: ") or default_format
    user_can_interface = input(f"Select CAN interface (can0/can1) [{default_can_interface}]: ") or default_can_interface
    
    # Configure your CAN interface
    bus = can.interface.Bus(bustype='socketcan', channel=user_can_interface, bitrate=500000)
    
    # Set up logging for the chosen format and get the path to the log file
    notifier, log_file_path = setup_logging(bus, user_format)
    
    try:
        print("Logging CAN messages. Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping logging...")
    finally:
        notifier.stop()
        bus.shutdown()
        print(f"Log files saved in {log_file_path}")

if __name__ == '__main__':
    main()
