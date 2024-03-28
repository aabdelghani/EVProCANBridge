import time
import can

def main():
    # Specify the channel (interface) you're using; can be 'can0' or 'can1'
    with can.interface.Bus(channel='can1', bustype='socketcan', receive_own_messages=True) as bus:
        print_listener = can.Printer()
        can.Notifier(bus, [print_listener])

        bus.send(can.Message(arbitration_id=1, is_extended_id=True))
        bus.send(can.Message(arbitration_id=2, is_extended_id=True))
        bus.send(can.Message(arbitration_id=1, is_extended_id=False))

        time.sleep(1.0)

if __name__ == "__main__":
    main()
