from gpiozero import LED

def setup(config):
    status_pin = int(config.get('GPIO', 'status_LED_pin'))
    mode_pin = int(config.get('GPIO', 'mode_LED_pin'))
    
    global statusLED, modeLED
    statusLED = LED(status_pin)
    modeLED = LED(mode_pin)
    

def setStatus(s):
    if s!=0:
        statusLED.on()
    else:
        statusLED.off()
    
def setMode(s):
    if s!=0:
        modeLED.on()
    else:
        modeLED.off()


def atexit():
    statusLED.off()
    modeLED.off()