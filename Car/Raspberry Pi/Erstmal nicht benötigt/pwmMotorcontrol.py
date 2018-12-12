import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library


def setup(config):
    GPIO.setmode(GPIO.BCM)  # Set Pi to use bcm number when referencing GPIO pins.

    global multiplier, motors
    multiplier = int(float(config.get('voltages', 'motor')) / float(config.get('voltages','battery')) * 100)

    motors = []
    for i in range(4):              # 4 Motoren und 4 Magnete #TODO 4 zu 8 ändern und die Magnete mit beachten
        motor = []
        for j in range(2):          # 2 Kabel pro Motor
            pin = int(config.get('GPIO', 'motor%d_pin%d') % (i, j))
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 100)   # Initialize PWM on pin 100Hz frequency
            pwm.start(0)
            motor.append(pwm)
        motors.append(motor)


def setMotorPower(motor, value):
    global motors
    if value < 0:
        value *= -1
        pwm1 = motors[motor][0]
        pwm2 = motors[motor][1]
    else:
        pwm1 = motors[motor][1]
        pwm2 = motors[motor][0]

    dc = value * multiplier
    pwm1.ChangeDutyCycle(dc)
    pwm2.ChangeDutyCycle(0)


def atexit():
    pwm.stop()                         # stop PWM
    GPIO.cleanup()                     # resets GPIO ports used back to input mode
