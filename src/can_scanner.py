import can
import time

def can_scanner(channel='can1', baud_rate=500000):
    """
    Scans for CAN messages on the specified channel and baud rate.
    
    Parameters:
    - channel (str): The CAN interface identifier (e.g., 'can0').
    - baud_rate (int): The baud rate of the CAN network.
    """
    # Setup CAN interface
    bus = can.interface.Bus(channel=channel, bustype='socketcan', bitrate=baud_rate)
    print(f"Scanning for CAN messages on {channel} at {baud_rate} baud rate...")
    
    try:
        while True:
            message = bus.recv(timeout=10)  # Adjust timeout as needed
            if message is not None:
                print(f"Received message: ID=0x{message.arbitration_id:X}, Data={message.data.hex()}, Timestamp={message.timestamp}")
            else:
                print("No message received within the timeout period.")
                # Optional: break or continue based on your needs
    except KeyboardInterrupt:
        print("Scanner stopped by user.")
    finally:
        bus.shutdown()

if __name__ == "__main__":
    # Example usage
    can_scanner(channel='can0', baud_rate=500000)
