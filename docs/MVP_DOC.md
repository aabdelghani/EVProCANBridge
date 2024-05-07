# Milestones Documentation

## Milestone 5: Dual CAN Connection and Recording at Startup

### Release Date
May 10, 2024

### Objectives
1. Configure dual CAN connections to interface with both BMS (Battery Management System) and EVC (Electric Vehicle Controller) on separate channels (CAN0 and CAN1) at different speeds (250kbps and 500kbps respectively).
2. Ensure both CAN interfaces begin logging immediately upon system startup.
3. Implement and refine a script (`setup_dual_can_logger_autostart.sh`) to automate the configuration and startup logging for both CAN interfaces.
4. Develop enhancements in `canLogger.py` to support simultaneous logging from both CAN interfaces with distinct configurations.

### Achievements
- **Dual CAN Configuration:** Successfully modified system settings to support BMS CAN on `CAN0` at 250kbps and EVC CAN on `CAN1` at 500kbps.
- **Simultaneous Logging at Startup:** Achieved automatic initiation of CAN logging from both interfaces at system boot, ensuring comprehensive data capture from the start.
- **AutoStart Configuration Script:** Created `setup_dual_can_logger_autostart.sh` that configures both CAN interfaces and ensures they are logged from on startup.
- **Updated Logging Capabilities:** Updated `canLogger.py` to handle simultaneous data capture and logging from two different CAN interfaces at varying speeds.

### Technical Details and References
- **Configuration Script:** `setup_dual_can_logger_autostart.sh` sets up CAN0 and CAN1 with specified speeds and adds commands to `/etc/rc.local` for automatic execution at boot.
- **Updated Logger Script:** Modifications in `canLogger.py` support differentiated logging processes for each CAN interface, accommodating the unique baud rates and data formats of BMS and EVC.
- **System Configuration Files:** Both CAN interfaces are configured through changes in `/etc/network/interfaces` and the respective systemd service units are managed to ensure persistent settings across reboots.

### Configuration and Usage
- The `setup_dual_can_logger_autostart.sh` script configures and activates logging for both CAN interfaces:
  ```bash
  bash setup_dual_can_logger_autostart.sh
  ```
- Each interface’s settings and operation can be verified using:
  ```bash
  cat /proc/sys/net/can
  ```
- Ensure proper operation of updated `canLogger.py` to handle simultaneous input from both CAN interfaces.

### References
- Systemd Documentation: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)
- Network Configuration for Linux: [https://www.networkconfiguration.com/](https://www.networkconfiguration.com/)
- Python-CAN Documentation: [https://python-can.readthedocs.io/en/stable/](https://python-can.readthedocs.io/en/stable/)

### Customer Feedback
- Pending ...

### Action Items
- [x] Test configuration stability for BMS and EVC CAN interfaces at their respective speeds.
- [x] Confirm logging initiates reliably at system boot.
- [ ] Collect and analyze customer feedback regarding the reliability and accuracy of the data logged.
- [ ] Evaluate potential for integrating more advanced diagnostic features into the logging software.

## Milestone 5: AutoStart for canLogger.py and CAN Frame Processing

### Release Date
April 8, 2024

### Objectives
1. Implement an auto-start mechanism for `canLogger.py` to ensure it runs at boot.
2. Develop a script (`setup_can_logger_autostart.sh`) to automate the insertion of `canLogger.py` execution into `rc.local`.
3. Create a script (`decode_can_frames_from_csv.py`) to convert raw CAN frame logs into a more comprehensible format (`human_readable_can_log.csv`).
4. Configure CAN interfaces automatically at boot using `can_setup.service`.

### Achievements
- **AutoStart Implementation:** Successfully configured `canLogger.py` to start automatically at system boot, ensuring continuous CAN frame logging.
- **AutoStart Setup Script:** Developed `setup_can_logger_autostart.sh`, which automates the process of adding `canLogger.py` to `rc.local` for execution at boot.
- **CAN Frame Decoding Script:** Introduced `decode_can_frames_from_csv.py`, which processes `csv_messages.csv` to generate `human_readable_can_log.csv`, improving readability and analysis.
- **CAN Interface Configuration Service:** Established `can_setup.service`, a systemd service designed to configure CAN interfaces (`can0` and `can1`) with specified settings at system boot.

### Technical Details and References
- **AutoStart Script:** `setup_can_logger_autostart.sh` adds a startup command to `/etc/rc.local`, leveraging the script's current directory to dynamically resolve paths.
- **Decoding Script Usage:** To run, navigate to the script directory and execute:
  ```bash
  python3 src/decode_can_frames_from_csv.py
  ```
  Ensure the Python environment is correctly set up and necessary libraries are installed.
- **CAN Setup Service:** `can_setup.service` uses systemd to ensure CAN interfaces are correctly configured at every boot, enhancing reliability and ease of use.

### Configuration and Usage
- The `can_setup.service` file is placed in `/etc/systemd/system/` and enabled via:
  ```bash
  sudo systemctl enable can_setup.service
  ```
- The `setup_can_logger_autostart.sh` script is executed once to configure auto-start settings:
  ```bash
  bash setup_can_logger_autostart.sh
  ```
- The `decode_can_frames_from_csv.py` script can be executed as needed to generate human-readable CAN logs.

### References
- Systemd Documentation: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)
- Python-CAN Documentation: [https://python-can.readthedocs.io/en/stable/](https://python-can.readthedocs.io/en/stable/)

### Customer Feedback
- Pending ...

### Action Items
- [x] Validate the effectiveness and reliability of the `can_setup.service`.
- [x] Ensure the auto-start mechanism via `rc.local` is robust across different system reboots.
- [ ] Gather customer feedback on the comprehensibility of the `human_readable_can_log.csv`.
- [ ] Explore further enhancements to CAN frame logging and processing capabilities.

## Milestone 4: Amperage and State of Charge (SOC) Broadcasting over CAN Bus

### Release Date
April 4, 2024

### Objectives
1. Make AMP Gauge work fine first, test, validate the code
2. Add AMP to SOC Gauges, test, validate the code 
3. Add level of configurability. `CANBus_Amp_and_BatteryLevel_Publisher.json` config file that you can configure both.
4. After finishing the above steps, we can add the Gauges in your cluster, one by one to our previously developed code.
5. Then we can make generic code to support all Gauges using the config file.

### Achievements
- **Dynamic Configuration:** Introduced a JSON-based configuration system allowing for easy adjustment of CAN parameters (ID, bitrate, AMP, and SOC range) without modifying the script code.
- **SOC and AMP Broadcasting Script:** Developed and successfully tested a Python script (`CANBus_Amp_and_BatteryLevel_Publisher.py`) that cycles through AMP values from -200 to 1201 and SOC values from 0% to 100%, broadcasting each value over the CAN bus.
- **Graceful Shutdown:** Enhanced the script with a mechanism for graceful shutdown upon receiving a keyboard interrupt (CTRL+C), ensuring clean script termination.
- All objectives were achieved, except for adding the Gauges in your cluster due to the unavailability of other gauges.

### Technical Details and References
- The AMP and SOC values are encoded and sent using specific CAN message structures, dictated by the `config/CANBus_Amp_and_BatteryLevel_Publisher.json` configuration file. This includes the start bit, bit length, scaling, and CAN ID in HEX format.
- Utilized the `python-can` library for CAN interface interaction, demonstrating a programmable method for sending CAN messages based on dynamic AMP and SOC values.
- Script execution and interruption are handled cleanly, providing feedback to the user upon shutdown.

### Configuration File Breakdown
The configuration file (`CANBus_Amp_and_BatteryLevel_Publisher.json`) includes several key parameters:
- `can_id_hex`: The CAN ID in hexadecimal format.
- `message_details`: Object specifying message encoding details such as start bit, bit length, scaling, and offset for both AMP and SOC values.
- `baud_rate`: The baud rate for CAN communication.
- `can_channel`: Specifies the CAN interface channel (e.g., `can0`).
- `amps_value_range`: Defines the range for cycling AMP values.
- `battery_level_range`: Defines the range for cycling SOC values.

### Script Usage
To run the script, navigate to the script's directory and execute:
```bash
python3 CANBus_Amp_and_BatteryLevel_Publisher.py
```
Ensure the CAN interface is correctly set up on your Raspberry Pi and the `python-can` library is installed.

### References
- [2-1/16" EV Amp Gauge -200 to 1200 (AEM)](https://speedhut.com/gauge-applications/2-1-16-ev-amp-gauge-200-to-1200-aem/?dd-link=0l8upv39raa)
- [Python-CAN Documentation](https://python-can.readthedocs.io/en/stable/)
- [2-1/16" EV Battery Level / SOC Gauge 0-100% (w/ warning) (AEM)](https://speedhut.com/gauge-applications/2-1-16-ev-battery-level-soc-gauge-0-100-w-warning-aem/?dd-link=0l8upv39raa)
- [EV_Gauge_Instructions - it has the CAN Message Format](https://github.com/aabdelghani/EVProCANBridge/blob/main/docs/2-116%20EV%20Battery%20Level%20%20SOC%20Gauge%200-100%20(w%20warning)%20(AEM).pdf)
  
### Customer Feedback
- The Battery level and AMP Gauge cluster are working perfectly based on the script `CANBus_Amp_and_BatteryLevel_Publisher.py` that utilized `can1` to send the battery percentage and AMP values with the needed config file.

### Action Items
- [x] Collect customer feedback on SOC and AMP broadcasting functionality.
- [x] Investigate enhancements for SOC and AMP message encoding and broadcasting efficiency.
- [x] Develop a generic script to support all gauges using the config file.
- [ ] Add the Gauges in your cluster one by one to our previously developed code (Pending due to unavailability of other gauges).


## Milestone 3: State of Charge (SOC) Broadcasting over CAN Bus

### Release Date
March 30, 2024

### Objectives
- Implement SOC broadcasting over the CAN bus using a Python script.
- Allow dynamic configuration of CAN message parameters through an external JSON file.
- Demonstrate cycling SOC values from 0% to 100% and broadcasting these over CAN.

### Achievements
- **Dynamic Configuration:** Introduced a JSON-based configuration system allowing for easy adjustment of CAN parameters (ID, bitrate, SOC range) without modifying the script code.
- **SOC Broadcasting Script:** Developed and successfully tested a Python script (`BatterySOC_CAN_Publisher.py`) that cycles through SOC values from 0% to 100%, broadcasting each value over the CAN bus.
- **Graceful Shutdown:** Enhanced the script with a mechanism for graceful shutdown upon receiving a keyboard interrupt (CTRL+C), ensuring clean script termination.

### Technical Details and References
- The SOC values are encoded and sent using a specific CAN message structure, dictated by the `config/BatterySOC_CAN_Publisher.json` configuration file. This includes the start bit, bit length, scaling, and CAN ID in HEX format.
- Utilized the `python-can` library for CAN interface interaction, demonstrating a programmable method for sending CAN messages based on dynamic SOC values.
- Script execution and interruption are handled cleanly, providing feedback to the user upon shutdown.

### Configuration File Breakdown
The configuration file (`BatterySOC_CAN_Publisher.json`) includes several key parameters:
- `can_id_hex`: The CAN ID in hexadecimal format.
- `message_details`: Object specifying message encoding details such as start bit, bit length, scaling, and offset.
- `baud_rate`: The baud rate for CAN communication.
- `can_channel`: Specifies the CAN interface channel (e.g., `can0`).
- `battery_percentage_range`: Defines the range for cycling SOC values.

### Script Usage
To run the script, navigate to the script's directory and execute:
```bash
python3 BatterySOC_CAN_Publisher.py
```
Ensure the CAN interface is correctly set up on your Raspberry Pi and the `python-can` library is installed.

### References
- [Python-CAN Documentation](https://python-can.readthedocs.io/en/stable/)
- [2-1/16" EV Battery Level / SOC Gauge 0-100% (w/ warning) (AEM)](https://speedhut.com/gauge-applications/2-1-16-ev-battery-level-soc-gauge-0-100-w-warning-aem/?dd-link=0l8upv39raa)
- [EV_Gauge_Instructions - it has the CAN Message Format](https://github.com/aabdelghani/EVProCANBridge/blob/main/docs/2-116%20EV%20Battery%20Level%20%20SOC%20Gauge%200-100%20(w%20warning)%20(AEM).pdf) 
  
### Customer Feedback
- The Battery level Gauge cluster working perfectly based on the script 'src/BatterySOC_CAN_Publisher.py' that utilized can1 to send the battery percentage from 0 to 100. with the needed config file

### Action Items
- [x] Collect customer feedback on SOC broadcasting functionality.
- [x] Investigate enhancements for SOC message encoding and broadcasting efficiency.
- [x] Develop the same script but make it work with the AMP Gauge 


# Milestone 2: Sending and Receiving CAN Messages with Physical Feedback
### Release Date
March 28, 2024

## Overview
Building on the success of the initial Milestone, which established reliable CAN communication on a Raspberry Pi, the next milestone (Milestone2) aims to demonstrate a practical application of CAN bus communication by creating and transmitting a specific CAN message from one interface and receiving it on another. Upon successful reception, a connected LED will be illuminated as a physical indicator of success.

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

## Script Functionality

The scripts developed as part of our project have specific functionalities tied to the Raspberry Pi's GPIO pins, particularly GPIO pin 17. One of the key scripts toggles the state of GPIO pin 17 to demonstrate physical interaction with the hardware. This is used as an indication of successful CAN message reception.


## How to Run the Scripts for Milestone2

### Prerequisites
Before running the scripts, ensure you have the following prerequisites installed on your Raspberry Pi:
- Python 3.x
- `python-can` library
- `RPi.GPIO` library (for the receiving script)
- Connecting LED to GPIO 17 

![GPIO Pin 17 Toggle](images/RaspberryPiPin17.jpg)

*Figure: Visual representation of GPIO pin 17 being toggled by the script.*

You can install the required Python libraries using pip:
```sh
pip3 install python-can RPi.GPIO
```

### Sending a CAN Message [send_can_message_v1.py](https://github.com/aabdelghani/EVProCANBridge/blob/main/send_can_message_v1.py) 
1. **Prepare the Script**: Make sure the [send_can_message_v1.py](https://github.com/aabdelghani/EVProCANBridge/blob/main/send_can_message_v1.py) script is saved on your Raspberry Pi.
2. **Run the Script**: Open a terminal and navigate to the directory containing the script. Execute the script by running:
   ```sh
   python3 send_can_message_v1.py
   ```
   This will send a predefined CAN message over the `can0` interface.

### Receiving CAN Messages and Toggling an LED [receive_can_message_v1.py](https://github.com/aabdelghani/EVProCANBridge/blob/main/recieve_can_messsage_v1.py)
1. **Hardware Setup**: Connect an LED to the designated GPIO pin on your Raspberry Pi. For the purposes of the script, we're using GPIO pin 17.
2. **Prepare the Script**: Ensure the `receive_can_message.py` script is saved on your Raspberry Pi, and it's configured to listen on the `can1` interface and to toggle the connected LED.
3. **Run the Script**: Open a new terminal window and navigate to the directory containing the `receive_can_message.py` script. Execute the script by running:
   ```sh
   python3 recieve_can_messsage_v1.py
   ```
   The script will listen for the specific CAN message. When the message is received, it will toggle the state of the LED.

### Note
- These scripts require administrative privileges to access the CAN interfaces and GPIO pins. If you encounter permission issues, prepend `sudo` to the Python command:
  ```sh
  sudo python3 send_can_message_v1.py
  ```
  ```sh
  sudo python3 receive_can_message.py
  ```

- To stop the scripts, especially the receiving script which runs in a loop, press `Ctrl+C` in the terminal.

This setup allows you to demonstrate the interaction between sending and receiving CAN messages and performing a physical action (toggling an LED) in response, illustrating the capabilities of your system in real-time.

### References
Pending

### Customer Feedback
Pending

### Action Items
- [x] **Define the CAN Message**: Specify the arbitration ID and data payload for the CAN message that will be used to trigger the LED.
- [x] **Develop Transmission Code**: Write and test the code that will send the specified CAN message over the `can0` interface.
- [x] **Develop Reception Code**: Implement the code that monitors incoming messages on the `can1` interface, looking specifically for the defined CAN message.
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

## Milestone 1: Running CAN Bus Communication Alongside Wireshark on Raspberry Pi

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
- [x] Gather customer feedback on the current Milestone functionality and usability.
- [x] Explore additional CAN bus analysis tools that can be integrated with the Raspberry Pi.
- [ ] Consider developing a more user-friendly interface for setting up CAN bus communication and monitoring.
