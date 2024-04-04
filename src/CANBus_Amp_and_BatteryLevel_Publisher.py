import can
import time

# Initialize the CAN bus
can_interface = 'can1'

try:
    bus = can.interface.Bus(can_interface, bustype='socketcan')
    
    # Initialize battery_level
    battery_level = 0

    while True:  # Make the entire process repeat indefinitely
        for amps_value in range(-200, 1202):  # From -200 to 1201 Amps
            raw_value = int(amps_value / 0.1)  # Apply scaling for Amps

            # Prepare the data bytes for both Amps and Battery Level
            data_bytes = bytearray(8)  # Start with 8 bytes of zeros
            
            # Incorporating Amps value
            data_bytes[2] = (raw_value >> 8) & 0xFF  # Higher byte for Amps
            data_bytes[3] = raw_value & 0xFF         # Lower byte for Amps
            
            # Incorporating Battery Level - fitting it into the byte considering Big Endian (Motorola) order
            data_bytes[1] = battery_level & 0xFF  # Direct assignment as it fits within a single byte

            # Create the CAN message
            msg = can.Message(arbitration_id=0x2F0A202,  # The ID HEX
                              data=data_bytes,           # The data we prepared
                              is_extended_id=True)       # Assuming extended ID due to the ID length

            # Send the message
            try:
                bus.send(msg)
                print(f"Message sent successfully: Amps Value = {amps_value}, Battery Level = {battery_level}%")
            except can.CanError:
                print(f"Failed to send message for Amps Value = {amps_value}, Battery Level = {battery_level}%")

            # Update battery_level for next iteration, cycling from 0 to 100
            battery_level = (battery_level + 1) % 101  # Ensure it cycles back to 0 after reaching 100

            time.sleep(1)  # Delay between messages

except KeyboardInterrupt:
    print("\nScript interrupted by user. Exiting...")
finally:
    print("Shutting down the bus")
    bus.shutdown()  # Explicitly shut down the bus
