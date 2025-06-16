import serial

ser = serial.Serial(
    port='/dev/serial0',  # Or ttyUSB0, depending on your wiring
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)

try:
    print("Listening for data...")
    while True:
        line = ser.readline()
        if line:
            print("Received:", line.decode('ascii', errors='replace').strip())
finally:
    ser.close()
