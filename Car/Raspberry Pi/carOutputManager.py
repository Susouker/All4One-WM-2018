import i2cManager as I2C
import pwmMotorcontrol as PWM

def setup(config):
    PWM.setup(config)
#    steeringFront, steeringBack, motor
lastAngles = (-180, -180, -180)
servoAdresses = (0x11, 0x12, 0x00)

def setServoAngles(car, r):
    if car == 'WM2017':
        oldCar(r)
    if car == 'P':
        prototyp(r)

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

def prototyp(r):
    PWM.setMotorPower([1][0])

def atexit():
    PWM.atexit
