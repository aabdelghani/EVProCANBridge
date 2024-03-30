
import can

def send_battery_level(channel):
    # Hardcoded values for the battery level message
    can_id = 0x2F0A202  # CAN ID for Battery Level
    battery_percentage = 50  # Example battery level to send
    
    # Encode the battery percentage into the data bytes according to the specification
    data_bytes = [0] * 8  # Initialize data payload with zeros
    data_bytes[1] = battery_percentage  # Place battery level at the correct position
    
    # Create and send the CAN message
    message = can.Message(arbitration_id=can_id,
                          data=data_bytes,
                          is_extended_id=True if can_id > 0x7FF else False)
    
    try:
        # Initialize the bus with the specified channel and baud rate
        with can.interface.Bus(channel=channel, bustype='socketcan', bitrate=500000) as bus:
            bus.send(message)
            print(f"Battery level message sent on {channel}.")
    except can.CanError:
        print(f"Failed to send message on {channel}.")

if __name__ == "__main__":
    # Send the battery level on both can0 and can1
    send_battery_level('can0')
    send_battery_level('can1')
