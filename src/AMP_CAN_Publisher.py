import can
import time

# Initialize the CAN bus
can_interface = 'can1'
bus = can.interface.Bus(can_interface, bustype='socketcan')

for amps_value in range(-200, 1201):  # From 0 to 1200 Amps
    raw_value = int(amps_value / 0.1)  # Apply scaling

    # Prepare the data bytes
    data_bytes = bytearray(8)  # Start with 8 bytes of zeros
    data_bytes[2] = (raw_value >> 8) & 0xFF  # Higher byte
    data_bytes[3] = raw_value & 0xFF        # Lower byte

    # Create the CAN message
    msg = can.Message(arbitration_id=0x2F0A202,  # The ID HEX
                      data=data_bytes,           # The data we prepared
                      is_extended_id=True)       # Assuming extended ID due to the ID length

    # Send the message
    try:
        bus.send(msg)
        print(f"Message sent successfully: {amps_value} Amps")
    except can.CanError:
        print(f"Failed to send message for {amps_value} Amps")

    time.sleep(0.1)  # Delay between messages, adjust as necessary
