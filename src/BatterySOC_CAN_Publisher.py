import can
import time
import json

def load_config():
    config_path = '../config/BatterySOC_CAN_Publisher.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def encode_battery_percentage(percentage, message_details):
    data_bytes = [0x00] * 8
    # Adjust the battery percentage according to the start bit and scaling
    data_bytes[message_details["start_bit"] // 8] = int((percentage - message_details["offset"]) * message_details["scaling"]) & 0xFF
    return bytes(data_bytes)

def send_can_message(bus, can_id, battery_percentage, message_details):
    data_payload = encode_battery_percentage(battery_percentage, message_details)
    message = can.Message(arbitration_id=can_id, data=data_payload, is_extended_id=True)
    
    try:
        bus.send(message)
        print(f"Message sent: ID=0x{can_id:X}, Battery Percentage={battery_percentage}%")
    except can.CanError:
        print("Message failed to send")

def cycle_battery_level(config):
    channel = config["can_channel"]
    baud_rate = config["baud_rate"]
    can_id = int(config["can_id_hex"], 16)  # Convert HEX ID to integer
    message_details = config["message_details"]
    start_percentage = config["battery_percentage_range"]["start"]
    end_percentage = config["battery_percentage_range"]["end"]

    try:
        with can.interface.Bus(channel=channel, bustype='socketcan', bitrate=baud_rate) as bus:
            while True:
                for percentage in range(start_percentage, end_percentage + 1):
                    send_can_message(bus, can_id, percentage, message_details)
                    time.sleep(1)  # Adjust as needed

                # Wait before restarting the cycle, if needed
                time.sleep(7)
    except KeyboardInterrupt:
        print("\nExecution stopped by user.")


if __name__ == "__main__":
    config = load_config()
    cycle_battery_level(config)
