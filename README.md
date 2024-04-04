# EVProCANBridge

The EVProCANBridge offers a cutting-edge solution designed to enhance the integration and communication between various components of electric vehicles (EVs). This tool bridges the gap between Battery Management Systems (BMS) and motor control units through dual isolated CAN channels, ensuring reliable and efficient vehicle operation.


## MVP Documentation

For detailed information on the development process, achievements, and technical approach of each MVP phase, please refer to our MVP documentation:

- [MVP Documentation](docs/MVP_DOC.md)

This document includes comprehensive details on the objectives, achievements, technical details, and references for each milestone of the project.

## References

- [2-Channel CAN-BUS FD Shield for Raspberry Pi - Seeed Studio Wiki](https://wiki.seeedstudio.com/2-Channel-CAN-BUS-FD-Shield-for-Raspberry-Pi/)
- [Python-CAN Documentation](https://python-can.readthedocs.io/en/stable/)

## Key Features


- **Dual CAN Interface**: Seamlessly integrates BMS (Battery Management System) and motor control functionalities, enabling efficient communication between these critical components.

- **Real-Time Data Processing**: Employs advanced algorithms for immediate processing of CAN messages, ensuring timely responses and adjustments for optimal vehicle control.

- **Comprehensive Data Logging**: Automatically captures and stores vital parameters such as voltage, temperature, and system errors, facilitating thorough diagnostics and maintenance.

- **Universal BMS Compatibility**: Designed with flexibility in mind, it supports a wide range of BMS protocols, making it adaptable to various EV models and systems.

- **Relay Control Module**: Introduces a layer of automation by executing predefined actions based on specific CAN messages or external signals, streamlining system operations.

- **Enhanced Safety Features**: Incorporates essential safety mechanisms including parking brake engagement, brake pedal verification for drive readiness, and a charging safety interlock to ensure EV security.

- **Simple Fleet Management Monitoring**: Offers straightforward solutions for fleet operators to monitor vehicle status, performance metrics, and maintenance needs, simplifying fleet management tasks.

## Getting Started

This section will guide you through the setup process and how to start using EVProCANBridge in your projects.

## General Configuration Rule for CAN Interfaces

To ensure reliable communication and the correct setup of CAN interfaces (`can0` and `can1`) on the Raspberry Pi, it is recommended to follow a standard procedure for shutting down and then re-initializing these interfaces with specific settings. This process is crucial for resetting the state of the CAN interfaces and applying new configurations such as bitrate changes or after making adjustments to network settings.

### Step-by-Step Procedure

1. **Shut Down Interfaces**: Begin by shutting down both `can0` and `can1` interfaces. This step ensures that any previous configurations are cleared, and the interfaces are in a known state before reconfiguration.
   
   Execute the following commands in the terminal:
   ```bash
   sudo ip link set can0 down
   sudo ip link set can1 down
   ```
   
2. **Re-initialize Interfaces**: After shutting down the interfaces, re-initialize them with the desired configuration settings. The example below sets both `can0` and `can1` to a bitrate of 500000 bits per second, a common configuration for many CAN networks.
   
   Use these commands to set the new configuration:
   ```bash
   sudo ip link set can0 up type can bitrate 500000
   sudo ip link set can1 up type can bitrate 500000
   sudo ifconfig can0 txqueuelen 65536
   sudo ifconfig can1 txqueuelen 65536
   ```

### Command Breakdown

- **`sudo`**: Executes commands with superuser privileges, necessary for network interface configuration.
- **`ip link set can0 down`** and **`ip link set can1 down`**: Commands to disable the `can0` and `can1` interfaces, clearing any active settings.
- **`ip link set can0 up type can bitrate 500000`** and **`ip link set can1 up type can bitrate 500000`**: Commands to re-enable the `can0` and `can1` interfaces with the `can` type and set the communication speed to 500,000 bits per second. The bitrate determines the rate at which data is transmitted over the CAN network and should be consistent across all devices on the network.
- **`sudo ifconfig can0 txqueuelen 65536`** and **`sudo ifconfig can1 txqueuelen 65536`**: These commands increase the transmit queue length for `can0` and `can1` to 65536. This adjustment can help manage data flow, especially in high traffic scenarios, by allowing more messages to be queued for transmission.

This configuration is critical for preparing the Raspberry Pi's CAN interfaces for communication tasks, ensuring that both `can0` and `can1` are properly set up to participate in CAN network activities with optimal performance and reliability.

### Prerequisites

- A Raspberry Pi 4 Model B Rev 1.5v.
- 2-Channel CAN-BUS(FD) Shield for Raspberry Pi (MCP2518FD)

**Important Configuration Note**: To ensure compatibility and optimal performance, you must configure your Raspberry Pi to run in 32-bit mode. This can be done by adding the line `arm_64bit=0` to the `/boot/config.txt` file on your Raspberry Pi. After adding this line, please restart your Raspberry Pi to apply the changes. This step is crucial for the proper functioning of the EVProCANBridge on the Raspberry Pi 4 Model B Rev 1.5v.

#### Built-in RTC Usage

The latest 2-Channel CAN FD Master Hat for RPi also includes an on-board RTC. To install the RTC drivers on your Raspberry Pi, follow these steps:

1. **Update Raspberry Pi and Reboot**:
    ```bash
    sudo apt update
    sudo apt upgrade
    sudo reboot
    ```

2. **Install Dependencies**:
    ```bash
    sudo apt install i2c-tools build-essential raspberrypi-kernel-headers
    ```

3. **Download the Driver**:
    ```bash
    curl -O -L https://github.com/dresden-elektronik/raspbee2-rtc/archive/master.zip
    unzip master.zip
    ```

4. **Compile the RTC Kernel Module**:
    ```bash
    cd raspbee2-rtc-master
    make
    ```

5. **Install the RTC Kernel Module**:
    ```bash
    sudo make install
    sudo reboot
    ```

6. **Configure System Time to the RTC Module**:
    ```bash
    sudo hwclock --systohc
    ```

7. **Test the RTC**:
    ```bash
    sudo hwclock --verbose
    ```

    Now you can read the RTC time using the following command:
    ```bash
    sudo hwclock -r
    ```

    **Note**: Ensure you have a battery installed on the RTC module for it to function correctly.


### Installation

Step-by-step guide to installing EVProCANBridge.

## Usage

Examples and tutorials on how to integrate and use EVProCANBridge in your EV projects.

