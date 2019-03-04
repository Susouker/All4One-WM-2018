import i2cManager as I2C
from math import *

last = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 0]
angleThreshold = 0.02     # 0.02rad sind etwa 1.15°
threshold = 0.05

LENKUNG    = 0b00100000
THROTTLE   = 0b01110000
VGC        = 0b00110000
VGCADJ     = 0b00111000
VGCADJSAVE = 0b00101000
TOWBAR     = 0b01100000

def setup(config):
    pass

def sendCarOutput(carOutput, forceSend):

    reverse = not carOutput[4] == 0
    if (reverse):
        dir = [3,2,1,0]
    else:
        dir = [0,1,2,3]

    global last
    for i in range(4):                                  # Für jedes Rad
        if abs(last[0][i] - carOutput[0][i]) > angleThreshold or forceSend == 1:       # Lenkwinkel
            v = (carOutput[0][i] + 1) * 128                      # -1rad - 1rad
            I2C.writeToSlave(LENKUNG + dir[i], v)
            last[0][i] = carOutput[0][i]

        if abs(last[1][i] - carOutput[1][i]) > threshold or forceSend == 2:            # Motorleisung
            v = min((carOutput[1][i] + 1) * 128, 255)
            I2C.writeToSlave(THROTTLE + dir[i], v)
            last[1][i] = carOutput[1][i]

        if abs(last[2][i] - carOutput[2][i]) > threshold or forceSend == 3:            # VGC
            v = min((carOutput[2][i]) * 256, 255)
            I2C.writeToSlave(VGC + dir[i], v)
            last[2][i] = carOutput[2][i]

    if abs(last[3] - carOutput[3]) > threshold or forceSend == 0:                      # Tow Bar
        v = min((carOutput[3]) * 256, 255)
        I2C.writeToSlave(TOWBAR, v)
        last[3] = carOutput[3]

def sendVGCadjustCommand(data):
    whatToAdj = data & 0b00000111
    value = data >> 3
    I2C.writeToSlave(VGCADJ + whatToAdj, value)
