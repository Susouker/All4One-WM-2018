import i2cManager as I2C

#    steeringFront, steeringBack, motor
lastAngles = (-180, -180, -180)
servoAdresses = (0x11, 0x12, 0x00)

def setServoAngles(car, R):
    if car == 'WM2017':
        oldCar(R)

def oldCar(R):
    global lastAngles
    
    steeringFront = R[0][0] + 90
    steeringBack = R[0][2] + 90
    motor = R[1][0] * 90 + 90

    angles = (steeringFront, steeringBack, motor)

    for i in range(3):
        if abs(angles[i] - lastAngles[i]) > 2:
            I2C.setServo(servoAdresses[i], angles[i])

    lastAngles = angles
