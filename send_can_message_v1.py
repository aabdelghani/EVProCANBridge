# Import the 'can' module from the python-can library
import can

def display_welcome():
    print("""
    Welcome to the CAN Message Sending Script!
    ------------------------------------------
    Author: Ahmed Abdelghany
	Email: ahmedabdelghany15@gmail.com

	Copyright (c) 2025 Vintage on Volt BV, Netherlands
	All rights reserved.
	
    This script sends a specific CAN message over the CAN bus using a designated interface.

    How it works:
    - Utilizes the 'can0' interface for sending messages.
    - Constructs a CAN message with a predefined arbitration ID and data payload.
    - Attempts to send the message over the CAN bus.
    - Notifies the user whether the message was successfully sent or if an error occurred.

    Usage:
    Simply run the script. There are no user inputs required. The script will automatically attempt to send the predefined CAN message and report on its success or failure.
    Please ensure that the 'python-can' library is installed and that the necessary CAN interface (e.g., 'can0') is properly configured on your system.
    Press Ctrl+C to exit the script if it's running in a loop or wait for the script to complete its execution.
    """)

# Define a function to send a CAN message
def send_can_message():
    # Specify the CAN interface (e.g., 'can0')
    can_interface = 'can0'
    
    # Use a 'with' statement for automatic cleanup. This ensures that the bus is properly closed
    # 'channel' specifies the CAN interface, 'bustype' specifies the type of bus (SocketCAN for Linux)
    with can.interface.Bus(channel=can_interface, bustype='socketcan') as bus:
        # Define the CAN message with an arbitration ID, data payload, and specify it's a standard ID (not extended)
        message = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
        
        # Try to send the CAN message
        try:
            # Send the message via the CAN bus
            bus.send(message)
            # Print a confirmation message including the interface and message details
            print("Message sent on {}: {}".format(can_interface, message))
        # Catch and print any errors during message sending
        except can.CanError:
            print("Message failed to send")

# Check if this script is executed as the main program and not imported as a module
if __name__ == "__main__":
	# Display the welcome message at the start
	display_welcome()  
    # Call the function to send the CAN message
	send_can_message()
