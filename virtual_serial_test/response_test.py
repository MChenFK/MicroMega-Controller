import serial
import time
import binascii

def main():
    port = '/dev/ttyUSB0'
    baudrate = 9600  # Check your controller manual
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        print(f"Listening on {port}...")

        while True:
            if ser.in_waiting:
                raw = ser.read_until(b'\r')  # Or read(32), depending on packet size
                print(f"Raw bytes: {raw}")
                print(f"Hex: {binascii.hexlify(raw)}")
                # Try decoding with latin1 just for inspection
                try:
                    print(f"Decoded (latin1): {raw.decode('latin1')}")
                except Exception as e:
                    print(f"Decode error: {e}")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
