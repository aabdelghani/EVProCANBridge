import can
from can import Listener, Notifier, CSVWriter

def main():
    # Specify the interface type (e.g., 'socketcan') and channel ('can1')
    bus = can.interface.Bus(channel='can1', bustype='socketcan')

    # Define the CSV file where messages will be saved
    log_filename = 'can_messages.csv'
    csv_writer = CSVWriter(log_filename)

    # Create a Notifier to distribute messages to the CSVWriter
    notifier = Notifier(bus, [csv_writer])

    try:
        # The notifier runs in a background thread, so keep the main thread alive
        print("Logging CAN messages to '{}'. Press Ctrl+C to stop.".format(log_filename))
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the notifier to flush messages to the CSV file
        notifier.stop()
        print("Logging stopped.")

if __name__ == "__main__":
    main()
