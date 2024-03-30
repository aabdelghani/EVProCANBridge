import can
import time
import json

def load_config():
    config_path = '../config/AMP_CAN_Publisher.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def encode_amperage(amps, message_details):
    data_bytes = [0x00] * 8
    # Adjust the amperage according to the start bit and scaling
    scaled_value = int((amps - message_details["offset"]) * message_details["scaling"])
    data_bytes[message_details["start_bit"] // 8] = scaled_value & 0xFF
    data_bytes[(message_details["start_bit"] // 8) + 1] = (scaled_value >> 8) & 0xFF
    return bytes(data_bytes)

def send_can_message(bus, can_id, amps, message_details):
    data_payload = encode_amperage(amps, message_details)
    message = can.Message(arbitration_id=can_id, data=data_payload, is_extended_id=True)
    
    try:
        bus.send(message)
        print(f"Message sent: ID=0x{can_id:X}, Amperage={amps} Amps")
    except can.CanError:
        print("Message failed to send")

def get_user_amperage():
    while True:
        try:
            amps = float(input("Enter the amperage (-200 to 1200): "))
            if -200 <= amps <= 1200:
                return amps
            else:
                print("Amperage must be between -200 and 1200.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def send_user_amperage(config):
    channel = config["can_channel"]
    baud_rate = config["baud_rate"]
    can_id = int(config["can_id_hex"], 16)
    message_details = config["message_details"]

    try:
        with can.interface.Bus(channel=channel, bustype='socketcan', bitrate=baud_rate) as bus:
            while True:
                amps = get_user_amperage()
                send_can_message(bus, can_id, amps, message_details)
                time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nExecution stopped by user.")

if __name__ == "__main__":
    config = load_config()
    send_user_amperage(config)
