import serial
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
    rtscts=True
)

try:
    time.sleep(0.01)

    ser.write(b'*01V\r')
    ser.flush()

    time.sleep(0.01)

    response = ser.readline()
    print("Response:", response.decode(errors='replace').strip())

finally:
    ser.close()
