address = {
0b00: 0x30, #Lenkservos, Radmotoren
0b01: 0x31, #VGC, cbTowBar
0b10: 0x32, #Bodyshell (Licht, Lichtsensor)
}

import consoleLog as CL
import smbus
import time
bus = smbus.SMBus(1)


def writeToSlave(identifier, value):
    slaveID = (identifier & 0b11000000) >> 6
    v = chr(int(value))
    try:
        bus.write_byte_data(adress[slaveID], identifier, v)
    except:
        CL.log(CL.ERROR, "During sending Data " + str(identifier) + ", " + str(value))
        return
