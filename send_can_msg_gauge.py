import can
import time

def send_can_message(bus, can_id, battery_percentage):
    """
    Send a CAN message with the specified battery percentage.

    Parameters:
    - bus (can.interface.Bus): The CAN bus object to send the message on.
    - can_id (int): CAN ID of the message to send.
    - battery_percentage (int): Battery level percentage to send.
    """
    # Initialize data payload with zeros and set battery percentage
    data_bytes = [0x00] * 8
    data_bytes[1] = battery_percentage  # Adjust this index if needed

    # Convert the list of integers to bytes
    data_payload = bytes(data_bytes)

    # Create a CAN message
    message = can.Message(arbitration_id=can_id,
                          data=data_payload,
                          is_extended_id=True)
    
    # Send the CAN message
    try:
        bus.send(message)
        print(f"Message sent: ID=0x{can_id:X}, Battery Percentage={battery_percentage}%")
    except can.CanError:
        print("Message failed to send")

def cycle_battery_level(channel='can0', baud_rate=500000, can_id=0x2F0A20):
    """
    Cycle the battery level from 0% to 100% and back down in a loop.

    Parameters:
    - channel (str): The CAN interface identifier. Adjust as necessary.
    - baud_rate (int): Baud rate of the CAN network.
    - can_id (int): CAN ID of the messages to send.
    """
    with can.interface.Bus(channel=channel, bustype='socketcan', bitrate=baud_rate) as bus:
        while True:
            # Increment battery level from 0 to 100
            for percentage in range(0, 101):
                send_can_message(bus, can_id, percentage)
                time.sleep(0.1)  # Delay between messages, adjust as necessary

            # Optional: Delay before starting the cycle again
            time.sleep(1)

if __name__ == "__main__":
    cycle_battery_level()
