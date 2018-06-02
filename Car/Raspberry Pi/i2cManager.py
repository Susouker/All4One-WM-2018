address_LS = 0x31
address_SC = 0x36

import consoleLog as cl
import smbus
import time
bus = smbus.SMBus(1)


def readLightSensor():
    data = 128
    try:
        data = bus.read_byte(address_LS) #12222222 1=aboveThreshold 2=value
    except:
        cl.log(cl.ERROR, "During reading i2c light sensor")
    b = data >> 7
    val = data & 127
    return (b, val)


def setLight(val, auto):
    data = (1 << 7) + (auto << 1) + val
    print(bin(data))
    bus.write_byte(address_LS, data) #10000234 1=L/B 2=Buzzer 3=LightAuto 4=Lighton/off

def setBuzzer(val):
    data = (0 << 7) + (val << 2)
    bus.write_byte(address_LS, data) #10000234 1=L/B 2=Buzzer 3=LightAuto 4=Lighton/off

def setServo(servo, val):
    try:
        bus.write_byte_data(address_SC, servo, val)
    except:
        cl.log(cl.ERROR, "During sending servo Data")
        return
