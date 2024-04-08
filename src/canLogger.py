import can
import json
import os
import subprocess  # Import subprocess module

def configure_can_interface(interface):
    # Command templates for setting up the CAN interface
    setup_commands = [
        f"sudo ip link set {interface} up type can bitrate 500000",
        f"sudo ifconfig {interface} txqueuelen 65536",
    ]
    
    for command in setup_commands:
        subprocess.run(command.split(), check=True)

def clean_up_can_interface(interface):
    # Command template for shutting down the CAN interface
    shutdown_command = f"sudo ip link set {interface} down"
    
    subprocess.run(shutdown_command.split(), check=True)
    print(f"{interface} has been shut down.")
    
    
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
        # Check if the file exists and is not empty to append without headers
        file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
        file_mode = 'a' if file_exists else 'w'
        # Open the file with the appropriate mode
        file_handle = open(filename, file_mode, newline='')  # newline='' is necessary for csv.writer to handle newlines correctly
        listener = can.CSVWriter(file_handle, lineterminator='\n')
    elif log_format == 'log':
        listener = can.CanutilsLogWriter(filename)
    elif log_format == 'trc':
        listener = can.TRCWriter(filename)
    
    # Attach the listener to a notifier
    notifier = can.Notifier(bus, [listener])
    
    return notifier, filename, lambda: file_handle.close() if log_format == 'csv' else None  # Return a cleanup function to close the file handle if necessary

def main():
    config = load_config()
    default_format = config.get("default_format", "csv")
    default_can_interface = config.get("default_can_interface", "can0")

    user_format = input(f"Enter the desired log format [{default_format}]: ") or default_format
    user_can_interface = input(f"Select CAN interface (can0/can1) [{default_can_interface}]: ") or default_can_interface

    configure_can_interface(user_can_interface)
    
    bus = can.interface.Bus(bustype='socketcan', channel=user_can_interface, bitrate=500000)
    
    # Initialize cleanup_func to None before setup_logging
    cleanup_func = None
    
    # Capture all three values returned by setup_logging
    notifier, log_file_path, cleanup_func = setup_logging(bus, user_format)
    
    try:
        print("Logging CAN messages. Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping logging...")
    finally:
        notifier.stop()
        bus.shutdown()
        clean_up_can_interface(user_can_interface)
        print(f"Log files saved in {log_file_path}")
        
        # Now cleanup_func is guaranteed to be defined, even if it's just None
        if cleanup_func:
            cleanup_func()

if __name__ == '__main__':
    main()
