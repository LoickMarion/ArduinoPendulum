import serial
import csv
import time

# Set the correct COM port and baud rate
COM_PORT = 'COM3'  # Replace with your Arduino's COM port (e.g., COM3, COM4, etc.)
BAUD_RATE = 9600   # Must match the baud rate set in Arduino code

# Open the serial connection
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE)
    print(f"Serial port {COM_PORT} opened successfully.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

time.sleep(2)  # Wait for the serial connection to establish

# Open CSV file to write the data
with open('sensor_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Start Time', 'End Time'])

    # Initialize counter
    data_count = 0
    max_data_points = 100  # Set the desired number of data points to collect

    # Continuously read serial data and write to CSV
    while data_count < max_data_points:
        if ser.in_waiting > 0:
            # Read data from Arduino
            data = ser.readline().decode('utf-8').strip()
            print(f"Data received: {data}")  # Debugging line
            
            # Split the data by the comma (assuming CSV format)
            values = data.split(', ')
            print(f"Data split into values: {values}")  # Debugging line
            
            # Write to CSV file
            writer.writerow(values)
            file.flush()  # Force the data to be written to the file immediately
            data_count += 1  # Increment the data count
            
            # Print count every 25 data points
            if data_count % 25 == 0:
                print(f"{data_count} data points written to CSV.")
            
            # Optional: Wait to avoid overwhelming the serial buffer
            time.sleep(0.1)

    print(f"Finished writing {data_count} data points to CSV.")
    
# Close the serial connection
ser.close()
