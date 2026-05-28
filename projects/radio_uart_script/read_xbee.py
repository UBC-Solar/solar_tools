import serial
import time

# Configuration parameters
SERIAL_PORT = '/dev/ttyUSB0'  # Update this if your FTDI cable is on a different port
BAUD_RATE = 230400              # XBee default baud rate

def monitor_uart():
    try:
        # Initialize the serial connection
        # timeout=1 ensures the script doesn't hang forever if no data arrives
        ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)
        
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        print("Listening for XBee data... (Press Ctrl+C to stop)")

        # Clear any garbage data that might be in the buffer from plugging it in
        ser.reset_input_buffer()

        while True:
            # Check if there are bytes waiting to be read
            if ser.in_waiting > 0:
                # Read the line, decode the raw bytes to UTF-8, and strip trailing newlines
                raw_data = ser.readline()
                try:
                    decoded_data = raw_data.decode('utf-8').rstrip()
                    print(f"Received: {decoded_data}")
                except UnicodeDecodeError:
                    # If the data isn't clean text (e.g., raw hex/binary payloads)
                    print(f"Received (Raw Hex): {raw_data.hex()}")

            # A small sleep prevents the while loop from maxing out your CPU
            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"Serial Port Error: {e}")
        print("Make sure the FTDI cable is plugged in and you have read permissions.")
    except KeyboardInterrupt:
        print("\nStopping monitor...")
    finally:
        # Always ensure the port is closed gracefully when exiting
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == '__main__':
    monitor_uart()