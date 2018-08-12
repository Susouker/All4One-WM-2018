import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

def setup(config):
    GPIO.setmode(GPIO.BCM)  # Set Pi to use pin number when referencing GPIO pins.
    global multiplier
    multiplier = int(float(config.get('voltages', 'motor')) / float(config.get('voltages','battery')) * 100)
    pwm = []

    pin1 = int(config.get('GPIO', 'motor1_pin1'))
    pin2 = int(config.get('GPIO', 'motor1_pin2'))
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    pwm.append(GPIO.PWM(pin1, 100))   # Initialize PWM on pwmPin 100Hz frequency/3
    pwm.append(GPIO.PWM(pin2, 100))   # Initialize PWM on pwmPin 100Hz frequency/3
    pwm[0].start(0)
    pwm[1].start(0)

# main loop of program
def setMotorPower(value):
    if value < 0:
        pwm1 = pwm[0]
        pwm2 = pwm[1]
    else:
        pwm1 = pwm[1]
        pwm2 = pwm[0]

    dc = value * multiplier
    pwm1.ChangeDutyCycle(dc)
    pwm2.ChangeDutyCycle(0)


def atexit():
    pwm.stop()                         # stop PWM
    GPIO.cleanup()                     # resets GPIO ports used back to input mode
