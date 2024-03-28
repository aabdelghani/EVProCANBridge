import can

def send_can_message():
    # Define the CAN interface to use (e.g., 'can0')
    can_interface = 'can0'
    
    # Create a bus connection on the specified interface
    bus = can.interface.Bus(channel=can_interface, bustype='socketcan')
    
    # Define a CAN message
    message = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
    
    # Send the message over the bus
    try:
        bus.send(message)
        print("Message sent on {}: {}".format(can_interface, message))
    except can.CanError:
        print("Message failed to send")

if __name__ == "__main__":
    send_can_message()
