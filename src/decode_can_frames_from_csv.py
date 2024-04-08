import base64
import csv
from datetime import datetime
import os

def convert_timestamp_to_readable(timestamp):
    """Converts a UNIX timestamp to a human-readable date-time string."""
    dt_object = datetime.utcfromtimestamp(float(timestamp))
    return dt_object.strftime('%Y-%m-%d %H:%M:%S.%f UTC')

def decode_can_frame(frame):
    """Decodes a CAN frame, converting the data field from base64 to hex."""
    timestamp, arbitration_id, extended, remote, error, dlc, data_encoded = frame
    
    data_decoded = base64.b64decode(data_encoded)
    data_as_hex = ' '.join([f'{byte:02x}' for byte in data_decoded])
    
    return timestamp, arbitration_id, extended, remote, error, dlc, data_as_hex

def process_can_messages(file_path):
    """Reads CAN messages, converts and decodes them, and writes to a new CSV."""
    output_directory = '../log'
    output_file_path = os.path.join(output_directory, 'human_readable_can_log.csv')
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    with open(file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        csv_writer = csv.writer(output_file, delimiter=',')
        
        # Assuming the first row is headers
        headers = ['timestamp', 'arbitration_id', 'extended', 'remote', 'error', 'dlc', 'data']
        csv_writer.writerow(headers)
        
        next(csv_reader, None)  # Skip the header of the input file
        for row in csv_reader:
            # Skip rows with repeated headers
            if row[0].lower() == 'timestamp':
                continue
            
            # Convert and decode the frame
            timestamp_readable = convert_timestamp_to_readable(row[0])
            _, arbitration_id, extended, remote, error, dlc, data_as_hex = decode_can_frame(row)
            
            # Write the processed row to the new file
            csv_writer.writerow([timestamp_readable, arbitration_id, extended, remote, error, dlc, data_as_hex])
    
    print(f'Processed file saved as: {output_file_path}')

# Example usage
file_path = '../log/can_messages.csv'  # Adjust this to the path of your input CSV file
process_can_messages(file_path)

