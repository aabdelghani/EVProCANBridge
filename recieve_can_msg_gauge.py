
import can

def receive_can_messages(channel='can1'):
    """
    Continuously receive and print CAN messages on a specified channel.

    Parameters:
    - channel (str): The CAN interface identifier. Typically 'can0', 'can1', etc.
    """
    # Configure the CAN interface
    try:
        bus = can.interface.Bus(channel=channel, bustype='socketcan')
        print(f"Listening for CAN messages on {channel}...")
    except Exception as e:
        print(f"Failed to open channel {channel}: {e}")
        return

    # Continuously listen for messages
    while True:
        message = bus.recv()  # This will block until a message is received
        if message is not None:
            print(f"Received message: ID=0x{message.arbitration_id:X}, "
                  f"Data={message.data.hex()}, "
                  f"Timestamp={message.timestamp}")

if __name__ == "__main__":
    # Start listening on can1
    receive_can_messages('can1')
