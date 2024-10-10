

import serial
import time

# Configure the serial port
# You may need to change the port name and baud rate to match your setup
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def send_command(command):
    """Send a command to the Arduino"""
    ser.write(command.encode())
    time.sleep(0.1)  # Give the Arduino some time to process

def read_response():
    """Read the response from the Arduino"""
    if ser.in_waiting > 0:
        return ser.readline().decode().strip()
    return None

def main():
    print("Arduino USB Communication")
    print("Type 'exit' to quit")

    while True:
        command = input("Enter command: ")
        if command.lower() == 'exit':
            break

        send_command(command)
        response = read_response()
        if response:
            print(f"Arduino response: {response}")
        else:
            print("No response from Arduino")

    ser.close()
    print("Communication ended")

