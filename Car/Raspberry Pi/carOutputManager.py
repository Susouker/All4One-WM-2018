import i2cManager as I2C
import pwmMotorcontrol as PWM

last = ((10, 10, 10, 10), (10, 10, 10, 10))
angleThreshold = 0.02     # 0.02rad sind etwa 1.15°
powerThreshold = 0.05


def setup(config):
    PWM.setup(config)


def setCarOutput(car, r):
    if car == 'WM2017':
        oldCar(r)
    if car == 'P':
        prototyp(r)


def prototyp(r):
    global last
    for i in range(4):                                  # Für jedes Rad

        if last[0][i] - r[0][i] > angleThreshold:       # Lenkwinkel
            I2C.setServo(i, r[0][i])                    # TODO Funktion anpassen, dass der Servotreiber aufgerufen wird
            last[0][i] = r[0][i]

        if last[1][i] - r[1][i] > powerThreshold:       # Motorleisung
            PWM.setMotorPower(i, r[1][i])
            last[1][i] = r[1][i]

        # TODO Magnete                                  # VGC Magnet
            # PWM.setMotorPower(i + 4, Magnet Power)


def atexit():
    PWM.atexit()


#Alte Methode. Nicht benutzen
servoAdresses = (0x11, 0x12, 0x00)
def oldCar(r):
    global lastAngles

    steeringFront = R[0][0] + 90
    steeringBack = R[0][2] + 90
    motor = R[1][0] * 90 + 90

    angles = (steeringFront, steeringBack, motor)

    for i in range(3):
        if abs(angles[i] - lastAngles[i]) > 2:
            I2C.setServo(servoAdresses[i], angles[i])

            lastAngles = angles
