import serial
import time
import struct

PORT = '/tmp/ttyV1'  # Change to match your test setup

# Simulated state
pv = 25.0     # Process Variable (e.g. temp)
sp = 50.0     # Setpoint
output = 50.0 # Output %

def modbus_crc(data):
    crc = 0xFFFF
    for ch in data:
        crc ^= ch
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')

def simulate_slave():
    global pv, sp, output
    ser = serial.Serial(PORT, baudrate=9600, bytesize=8, stopbits=1, parity='N', timeout=1)
    print(f"Listening on {PORT}...")

    while True:
        request = ser.read(8)
        if len(request) < 8:
            continue

        slave_id, func_code = request[0], request[1]
        addr = request[2] << 8 | request[3]

        if func_code == 3:  # Read Holding Registers
            num_regs = request[4] << 8 | request[5]

            # Update PV and output for realism
            pv += 0.1
            if pv > 100: pv = 0
            output = (pv / sp) * 100 if sp > 0 else 0

            # Simulated data
            reg_map = {
                0: int(pv),       # Register 0: PV
                1: int(sp),       # Register 1: SP
                2: int(output),   # Register 2: Output
            }

            response_regs = []
            for i in range(addr, addr + num_regs):
                response_regs.extend(divmod(reg_map.get(i, 0), 0x100))  # big endian

            response = bytes([slave_id, 3, len(response_regs)]) + bytes(response_regs)
            ser.write(response + modbus_crc(response))

        elif func_code == 6:  # Write Single Register
            reg_addr = request[2] << 8 | request[3]
            value = request[4] << 8 | request[5]

            if reg_addr == 1:  # Update setpoint
                sp = float(value)
                print(f"Setpoint updated to {sp}")

            # Echo response back (standard behavior)
            ser.write(request + modbus_crc(request))

        time.sleep(0.1)

if __name__ == '__main__':
    simulate_slave()
