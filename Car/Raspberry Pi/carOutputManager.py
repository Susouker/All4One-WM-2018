import i2cManager as I2C

last = [[10, 10, 10, 10], [10, 10, 10, 10], [10, 10, 10, 10], 10]
angleThreshold = 0.02     # 0.02rad sind etwa 1.15°
threshold = 0.05

LENKUNG   = 0b00100000
THROTTLE  = 0b00110000
VGC       = 0b01100000
TOWBAR    = 0b01110000

def setup(config):
    pass


def setCarOutput(car, carOutput):
    if car == 'P':
        prototyp(carOutput)


def prototyp(carOutput):
    global last
    for i in range(4):                                  # Für jedes Rad
        if abs(last[0][i] - carOutput[0][i]) > angleThreshold:       # Lenkwinkel
            v = (carOutput[0][i] + 1) * 128                      # -1rad - 1rad
            I2C.writeToSlave(LENKUNG + i, v)
            last[0][i] = carOutput[0][i]

        if abs(last[1][i] - carOutput[1][i]) > threshold:            # Motorleisung
            v = (carOutput[1][i] + 1) * 128
            I2C.writeToSlave(THROTTLE + i, v)
            last[1][i] = carOutput[1][i]

        if abs(last[2][i] - carOutput[2][i]) > threshold:            # VGC
            v = (carOutput[2][i]) * 256
            I2C.writeToSlave(VGC + i, v)
            last[2][i] = carOutput[2][i]

    if abs(last[3] - carOutput[3]) > threshold:                      # Tow Bar
        v = (carOutput[3] + 1) * 128
        I2C.writeToSlave(TOWBAR, v)
        last[3] = carOutput[3]
