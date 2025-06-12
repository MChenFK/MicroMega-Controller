from pymodbus.client.serial import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    #port='/dev/ttyUSB0',
    port = /tmp/ttyV0
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

if client.connect():
    result = client.read_holding_registers(address=0, count=2, unit=1)
    if result.isError():
        print("Modbus Error:", result)
    else:
        print("Registers:", result.registers)
    client.close()
else:
    print("Connection failed")
