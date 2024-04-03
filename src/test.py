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
    # Calculate the byte index and the bit position within that byte
    byte_index = message_details["start_bit"] // 8
    bit_position = message_details["start_bit"] % 8
    
    # Encode the amperage value considering offset and scaling
    raw_value = int((amperage - message_details["offset"]) / message_details["scaling"])
    
    # Check if the type is 'Signed' and perform a 2's complement if needed
    if message_details["type"] == 'Signed' and raw_value < 0:
        raw_value = (1 << message_details["bit_length"]) + raw_value
    
    # Split the raw_value into two bytes (16 bits)
    low_byte = raw_value & 0xFF
    high_byte = (raw_value >> 8) & 0xFF
    
    # Place the low_byte and high_byte into the correct position within the CAN data
    # taking into account that the data might start in the middle of a byte
    data_bytes[byte_index] |= (low_byte << bit_position) & 0xFF
    data_bytes[byte_index + 1] |= (high_byte >> (8 - bit_position)) & 0xFF
    
    # If the value spreads over more than two bytes, set the next byte as well
    if bit_position > 0:
        data_bytes[byte_index + 2] |= (high_byte << bit_position) & 0xFF
    
    return bytes(data_bytes)


def send_can_message(bus, can_id, amps, message_details):
    data_payload = encode_amperage(amps, message_details)
    message = can.Message(arbitration_id=can_id, data=data_payload, is_extended_id=True)
    
    try:
        bus.send(message)
        print(f"Message sent: ID=0x{can_id:X}, Amperage={amps} Amps")
    except can.CanError:
        print("Message failed to send")

def cycle_amperage(config):
    channel = config["can_channel"]
    baud_rate = config["baud_rate"]
    can_id = int(config["can_id_hex"], 16)  # Convert HEX ID to integer
    message_details = config["message_details"]
    start_amperage = config["amperage_range"]["start"]
    end_amperage = config["amperage_range"]["end"]
    step_amperage = 10  # Increment amperage by 10

    try:
        with can.interface.Bus(channel=channel, bustype='socketcan', bitrate=baud_rate) as bus:
            while True:
                for amps in range(start_amperage, end_amperage + 1, step_amperage):
                    send_can_message(bus, can_id, amps, message_details)
                    time.sleep(0.2)  # Adjust as needed

                # Wait before restarting the cycle, if needed
                time.sleep(7)
    except KeyboardInterrupt:
        print("\nExecution stopped by user.")

if __name__ == "__main__":
    config = load_config()
    cycle_amperage(config)
