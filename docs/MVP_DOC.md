# MVP Documentation
# MVP 2: Sending and Receiving CAN Messages with Physical Feedback
### Release Date
March 28, 2024

## Overview
Building on the success of the initial MVP, which established reliable CAN communication on a Raspberry Pi, the next milestone (MVP2) aims to demonstrate a practical application of CAN bus communication by creating and transmitting a specific CAN message from one interface and receiving it on another. Upon successful reception, a connected LED will be illuminated as a physical indicator of success.

## Objectives
- Create a specific CAN message to be sent over the CAN bus.
- Transmit the message from CAN0 interface.
- Receive the message using the CAN1 interface.
- Use the reception of the message as a trigger to turn on an LED, providing a visual indication of successful communication.

## Technical Approach
1. **Message Creation**: Define a unique CAN message with a specific arbitration ID and data payload.
2. **Transmission**: Use the configured `can0` interface to send the created message into the CAN network.
3. **Reception**: Continuously monitor the `can1` interface for incoming messages. When the specific message is detected, trigger a GPIO pin on the Raspberry Pi to turn on an LED.
4. **Feedback**: Implement a simple feedback mechanism to visually indicate the success of the message transmission and reception process.

### References
Pending

### Customer Feedback
Pending

### Action Items
- [ ] **Define the CAN Message**: Specify the arbitration ID and data payload for the CAN message that will be used to trigger the LED.
- [ ] **Develop Transmission Code**: Write and test the code that will send the specified CAN message over the `can0` interface.
- [ ] **Develop Reception Code**: Implement the code that monitors incoming messages on the `can1` interface, looking specifically for the defined CAN message.
- [ ] **Hardware Setup**: Connect an LED to the appropriate GPIO pin on the Raspberry Pi, ensuring it can be controlled programmatically.
- [ ] **Implement LED Control Logic**: Integrate the LED control logic into the reception code, so the LED turns on when the specified CAN message is received.
- [ ] **Testing**: Perform comprehensive testing to ensure:
    - The CAN message is correctly formatted and sent over `can0`.
    - The message is accurately received by `can1` without errors.
    - The LED correctly responds to the reception of the message.
- [ ] **Documentation**: Update the project documentation to include:
    - Technical details of the CAN message used.
    - Descriptions of the transmission and reception code.
    - Wiring instructions for connecting the LED to the Raspberry Pi.
    - A troubleshooting guide covering common issues and their resolutions.

## MVP 1: Running CAN Bus Communication Alongside Wireshark on Raspberry Pi

### Release Date
March 27, 2024

### Objectives
- Establish reliable CAN bus communication on Raspberry Pi.
- Monitor CAN bus traffic using Wireshark for analysis and debugging.
- Demonstrate successful installation and execution of Python scripts for CAN bus interaction.

### Achievements
- **CAN Interface Setup:** Configured `can0` and `can1` with specific bitrates and settings for CAN FD.
- **Communication Testing:** Successfully tested CAN FD protocol communication between `can0` and `can1` using `cangen` and `candump` commands.
- **Python-CAN Integration:** Installed python-can library and ran a Python script to receive CAN data, demonstrating programmable interaction with the CAN bus.

### Technical Details and References
- Configured CAN interfaces `can0` and `can1` on the Raspberry Pi using the following commands:
  ```bash
  sudo ip link set can0 up type can bitrate 1000000 dbitrate 8000000 restart-ms 1000 berr-reporting on fd on
  sudo ip link set can1 up type can bitrate 1000000 dbitrate 8000000 restart-ms 1000 berr-reporting on fd on
  sudo ifconfig can0 txqueuelen 65536
  sudo ifconfig can1 txqueuelen 65536
  
## Command Breakdown

- **`sudo`**: Allows running programs with the security privileges of another user, by default the superuser. It's necessary for configuring network interfaces due to the administrative privileges required.

- **`ip link set can0 up`**: Uses the `ip` tool to configure network interfaces. It activates the interface named `can0`, typically the first CAN interface on the system.

- **`type can`**: Specifies the interface type as CAN, a standard designed for microcontrollers and devices to communicate without a host computer.

- **`bitrate 1000000`**: Sets the bitrate for standard CAN frames to 1 Mbps (Mega-bits per second), dictating the speed of data transmission over the CAN network.

- **`dbitrate 8000000`**: Establishes the bitrate for the data phase of CAN FD frames to 8 Mbps. CAN FD, an extension of the original CAN, supports a higher data rate.

- **`restart-ms 1000`**: Defines the automatic retransmission delay to 1000 milliseconds (1 second) in case of bus errors, allowing the system to retry transmission after a brief pause.

- **`berr-reporting on`**: Enables reporting of bus errors, providing diagnostics and error-tracking capabilities for the CAN bus.

- **`fd on`**: Activates support for CAN FD on the interface, allowing for the usage of CAN FD frames that offer increased data capacity and potentially higher data rates than standard frames.

This configuration ensures that the `can0` interface is optimized for performance and reliability, adhering to modern CAN and CAN FD standards.

- Tested CAN FD protocol using `cangen` and `candump`, indicating successful communication setup.
- Attempted to use python-can for CAN data reception, facing initial issues with the script from Seeed Studio documentation.
- Resolved the script issues by following the python-can documentation, leading to successful data reception and sending.

### References
- [2-Channel CAN-BUS FD Shield for Raspberry Pi - Seeed Studio Wiki](https://wiki.seeedstudio.com/2-Channel-CAN-BUS-FD-Shield-for-Raspberry-Pi/)
- [Python-CAN Documentation](https://python-can.readthedocs.io/en/stable/)
- [Python-CAN Listeners and Notifiers Example](https://python-can.readthedocs.io/en/stable/listeners.html)

### Customer Feedback
Pending

### Action Items
- [x] Gather customer feedback on the current MVP functionality and usability.
- [x] Explore additional CAN bus analysis tools that can be integrated with the Raspberry Pi.
- [ ] Consider developing a more user-friendly interface for setting up CAN bus communication and monitoring.
