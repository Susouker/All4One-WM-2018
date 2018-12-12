from gpiozero import LED
lastPulse = 0

def setup(config):
    status_pin = int(config.get('GPIO', 'status_LED_pin'))
    mode_pin = int(config.get('GPIO', 'mode_LED_pin'))

    global statusLED, modeLED, lastPulse
    statusLED = LED(status_pin)
    statusLED.on()
    modeLED = LED(mode_pin)


def setMode(s):
    if s!=0:
        modeLED.on()
    else:
        modeLED.off()

def update(time):
    global lastPulse
    if time - lastPulse > 0.5:
        statusLED.toggle()
        lastPulse = time


def atexit():
    statusLED.off()
    modeLED.off()
