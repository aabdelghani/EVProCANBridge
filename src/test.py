import can
import time
import json

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def encode_data(amps_value, battery_level):
    data_bytes = bytearray(8)  # Initialize with zeros
    raw_value = int(amps_value / 0.1)  # Apply scaling for Amps
    # Incorporate the Amps value
    data_bytes[2] = (raw_value >> 8) & 0xFF
    data_bytes[3] = raw_value & 0xFF
    # Incorporate the Battery Level
    data_bytes[1] = battery_level & 0xFF
    return data_bytes

def send_can_message(bus, arbitration_id, amps_value, battery_level):
    data_bytes = encode_data(amps_value, battery_level)
    msg = can.Message(arbitration_id=arbitration_id, data=data_bytes, is_extended_id=True)
    try:
        bus.send(msg)
        print(f"Message sent successfully: Amps Value = {amps_value}, Battery Level = {battery_level}%")
    except can.CanError:
        print(f"Failed to send message for Amps Value = {amps_value}, Battery Level = {battery_level}%")

def main():
    config = load_config('../config/test.json')  # Update the path to your config file
    arbitration_id = int(config['arbitration_id_hex'], 16)
    battery_level = config['battery_level_range']['start']

    try:
        bus = can.interface.Bus(config['can_interface'], bustype='socketcan')
        while True:
            for amps_value in range(config['amps_value_range']['start'], config['amps_value_range']['end'] + 1):
                send_can_message(bus, arbitration_id, amps_value, battery_level)
                # Update battery_level for next iteration, cycling from 0 to 100
                battery_level = (battery_level + 1) % (config['battery_level_range']['end'] + 1)
                time.sleep(config['message_delay_seconds'])
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        print("Shutting down the bus")
        bus.shutdown()

if __name__ == "__main__":
    main()
