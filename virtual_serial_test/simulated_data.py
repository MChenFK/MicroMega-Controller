import serial
import time

PORT = '/dev/ttyV1'

def modbus_crc(data):
    crc = 0xFFFF
    for ch in data:
        crc ^= ch
        for _ in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc.to_bytes(2, 'little')

def simulate_slave():
    ser = serial.Serial(PORT, baudrate=9600, bytesize=8, stopbits=1, parity='N', timeout=1)
    print(f"Listening on {PORT}...")
    while True:
        request = ser.read(8)  # Typical Modbus RTU request size
        if not request:
            continue

        slave_id = request[0]
        func_code = request[1]
        address_hi = request[2]
        address_lo = request[3]
        reg_count_hi = request[4]
        reg_count_lo = request[5]

        print(f"Received: {request.hex()}")

        # Dummy data response for Read Holding Registers (function code 3)
        if func_code == 3:
            num_regs = reg_count_hi << 8 | reg_count_lo
            byte_count = num_regs * 2
            fake_data = [0x00, 0x64] * num_regs  # simulate 100 in each register

            response = bytes([slave_id, func_code, byte_count] + fake_data)
            crc = modbus_crc(response)
            ser.write(response + crc)
            print(f"Sent: {(response + crc).hex()}")

        time.sleep(0.1)

if __name__ == '__main__':
    simulate_slave()
