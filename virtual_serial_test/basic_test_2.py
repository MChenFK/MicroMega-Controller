import serial
import time
import logging

# Configure logging
logging.basicConfig(
    filename="pid_comm_log.txt",
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

# Serial port and device settings
PORT = '/dev/serial0'
BAUDRATE = 9600
DEVICE_ADDRESS = "00"  # RS-485 address of your device
RECOGNITION_CHAR = "*"

def main():
    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            rtscts=True,
            dsrdtr=True
        )
        print(f"Connected to {ser.port}. Type command suffixes (e.g., R01, Z02, W01A003E8). Type 'exit' to quit.")

        while True:
            user_input = input("Command> ").strip()
            if user_input.lower() == "exit":
                break

            # Ensure command starts with "*00"
            if not user_input.startswith(RECOGNITION_CHAR + DEVICE_ADDRESS):
                full_cmd = f"{RECOGNITION_CHAR}{DEVICE_ADDRESS}{user_input}"
            else:
                full_cmd = user_input

            # Ensure it ends with carriage return
            if not full_cmd.endswith('\r'):
                full_cmd += '\r'

            # Send command
            ser.write(full_cmd.encode())
            logging.info(f"Sent: {repr(full_cmd)}")

            # Wait and read response
            time.sleep(0.5)
            response = ser.read_all()
            print("Raw:", repr(response))

            decoded = response.decode(errors='ignore').strip()
            print("Decoded:", decoded)
            logging.info(f"Received: {response}")

        ser.close()

    except serial.SerialException as e:
        error_msg = f"Serial error on {PORT}: {e}"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    main()
