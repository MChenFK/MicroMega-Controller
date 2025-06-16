from pymodbus.client.serial import ModbusSerialClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
import logging
import time

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

client = ModbusSerialClient(
    method='rtu',
    framer=ModbusRtuFramer,
    port='/dev/serial0',
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

if client.connect():
    print("Connected to Modbus slave")

    # PV at register 4095, SV at 4096 → zero-indexed address = 4095
    result = client.read_holding_registers(address=1, count=2, unit=0)
    if result.isError():
        print("Modbus Error:", result)
    else:
        pv, sv = result.registers
        print(f"PV: {pv}, SV: {sv}")

    client.close()
else:
    print("Connection failed")
