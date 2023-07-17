from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ConnectionException
from pymodbus.exceptions import ModbusException
import threading

def connect_modbus(port, stopbits, bytesize, parity, baudrate):
    status = False
    client = ModbusSerialClient(
        method = 'rtu',
        port=port,
        stopbits=stopbits,
        bytesize=bytesize,
        parity=parity,
        baudrate=baudrate
    )

    client.connect()
    result = client.read_holding_registers(
        address=0x0,
        count=0x20,
        unit=0x1
    )

    if not result.isError():
        status = True
    else:
        status = False

    
    return status

def test():
    client = ModbusSerialClient(
        method = 'rtu',
        port="COM4",
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=115200
    )

    try :
        client.connect()
        print("successfully connect")
    except :
        print("Cant connect")


    
    result = client.read_holding_registers(
        address=0x0,
        count=0x20,
        unit=0x1
    )
    print(result.registers)
    print(result.registers[19]/10)


if __name__ == '__main__':
    test()

        
    