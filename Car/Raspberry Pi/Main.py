CONFIG_URL = "config.conf"
SENDRATE = 0.005

#--------------------INITIALSETUP--------------------
if __name__ == '__main__':
    from math import *
    import struct
    import time
    import consoleLog as CL
    import configparser

    CL.log(CL.INFO, "Beginning initialsetup")

    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_URL)
        CL.log(CL.INFO, "Config file read")
    except:
        CL.log(CL.ERROR, "while loading config")

    PROPERTIES = []
    if int(config.get('input', 'visualizer')):
        PROPERTIES.append('VISUALIZER_AS_INPUT')
    if int(config.get('input', 'socket')):
        PROPERTIES.append('SOCKET_AS_INPUT')
    if 'VISUALIZER_AS_INPUT' in PROPERTIES or int(config.get('output', 'visualizer')):
        PROPERTIES.append('USE_VISUALIZER')
    if int(config.get('output', 'GPIO')):
        PROPERTIES.append('USE_GPIO')

    import relativeMotion
    import VGC
    import server
    import optionManager
    if 'USE_VISUALIZER' in PROPERTIES:
        import visualizer
    if 'USE_GPIO' in PROPERTIES:
        import carOutputManager
    if 'USE_GPIO' in PROPERTIES:
        import gpioManager as GPIO

#--------------------LOOP--------------------
def loop():
    try:
        global startTime, lastSend, IS_ACTIVE

        #Get input from Mouse Curosr if visualizer is used
        if 'VISUALIZER_AS_INPUT' in PROPERTIES:
            try:
                setInput(*visualizer.getInput())
            except:
                IS_ACTIVE = False
                return

        #Update
        if 'USE_VISUALIZER' in PROPERTIES:
            global rChanged
            if rChanged:
                rChanged = 0
                visualizer.setInput(carOutput)
            visualizer.update()
        if 'USE_GPIO' in PROPERTIES:
            GPIO.upadate(time.time() - startTime)

    except KeyboardInterrupt:
        IS_ACTIVE = False
        return

def getR():
    return r

def setCarOutput(category, value, update):
    global carOutput
    carOutput[category] = value

    if update:
        if 'USE_VISUALIZER' in PROPERTIES:
            global rChanged
            rChanged = 1

        if 'USE_GPIO' in PROPERTIES:
            carOutputManager.setCarOutput('P', carOutput)

        #Send Data Back over TCP
        if (time.time() - startTime - lastSend) > (1/SENDRATE):
            global lastSend
            server.sendData(b'A' ,struct.pack('4f', *r[0]))
            server.sendData(b'T' ,struct.pack('4f', *r[1]))
            lastSend += 1/SENDRATE

def setInput(input, steeringMode):
    global carOutput, rChanged
    if steeringMode == 0:
        r = relativeMotion.calcS(input[0], input[2])
    elif steeringMode == 1:
        r = relativeMotion.calcC(input[0], input[1], input[2])

    setCarOutput(0, r[0], False)
    setCarOutput(1, r[1], True)


#--------------------SETUP--------------------
def setup():
    CL.log(CL.INFO, "Beginning setup")
    globalVars()
    CL.log(CL.INFO, PROPERTIES)

    server.setup(config, [setInput, optionManager.setProperty, getR, VGC.setMode])
    relativeMotion.setup(config)
    VGC.setup(config)
    if 'USE_GPIO' in PROPERTIES:
        GPIO.setup(config)
        carOutputManager.setup(config)
    if 'USE_VISUALIZER' in PROPERTIES:
        visualizer.setup(config)

    CL.log(CL.INFO, "setup is complete")


def globalVars():
    global IS_ACTIVE, carOutput, startTime, lastSend
    IS_ACTIVE = True
    carOutput = (
    (0,0,0,0),  # Lenkwinkel
    (0,0,0,0),  # Throttle
    (0,0,0,0),  # VGC
    0.5,        # Tow Bar
    )
    startTime = time.time()
    lastSend = startTime


if __name__ == '__main__':
    setup()
    setInput((0, 0, 0), 0)
    CL.log(CL.INFO, "loop starting")
    while IS_ACTIVE:
        loop()
    CL.log(CL.INFO, "loop stopping")
    if 'USE_GPIO' in PROPERTIES:
        GPIO.atexit()
