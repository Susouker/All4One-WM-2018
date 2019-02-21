address = {
0b00: 0x30, #Lenkservos, Radmotoren
0b01: 0x31, #VGC, cbTowBar
0b10: 0x32, #Bodyshell (Licht, Lichtsensor)
}

import consoleLog as CL
import smbus2
import time
bus = smbus2.SMBus(1)

disabledAddresses = []

def writeToSlave(identifier, value):
    slaveID = (identifier & 0b11000000) >> 6
    v = int(value)
    try:
        bus.write_byte_data(address[slaveID], identifier, v)
    except OSError:
        if not address[slaveID] in disabledAddresses:
            CL.log(CL.ERROR, "During sending Data; " + str(address[slaveID]))
            disabledAddresses.append(address[slaveID])
