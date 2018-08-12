CONFIG_URL = "config.conf"
LOGGING = False
SENDRATE = 0.005
LOGRATE = 5

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
    if 'USE_VISUALIZER' in PROPERTIES:
        import visualizer
    if 'USE_GPIO' in PROPERTIES:
        import i2cManager as I2C
        import servoAngles
    if 'USE_GPIO' in PROPERTIES:
        import gpioManager as GPIO
    if 'LOGGING' in PROPERTIES:
        import logger


#--------------------LOOP--------------------
def loop():
    try:
        global startTime, lastSend, lastLog, IS_ACTIVE

        #Get input from Mouse Curosr if visualizer is used
        global input, light
        if 'VISUALIZER_AS_INPUT' in PROPERTIES:
            try:
                setInput(visualizer.getInput())
            except:
                IS_ACTIVE = False
                return

        #Update
        if 'USE_VISUALIZER' in PROPERTIES:
            global rChanged
            if rChanged:
                rChanged = 0
                visualizer.setInput(r, light)
            visualizer.update()

        if LOGGING and (time.time() - startTime - lastLog) > (1/LOGRATE):
            LO.log(currentTime, light, input, r)
            lastLog += 1/LOGRATE

    except KeyboardInterrupt:
        IS_ACTIVE = False
        return


def setInput(input, steeringMode):
    print(degrees(input[0]))
    global r, rChanged
    if steeringMode == 0:
        r = relativeMotion.calcS(input[0], input[2])
    if steeringMode == 1:
        r = relativeMotion.calcC(input[0], input[1], input[2])
    if steeringMode == -1:
        r = relativeMotion.calcES(input[0], input[2])

    if 'USE_VISUALIZER' in PROPERTIES:
        rChanged = 1

    if 'USE_GPIO' in PROPERTIES:
        SA.setServoAngles('WM2017', r)

    #Send Data over TCP
    global lastSend, startTime
    if (time.time() - startTime - lastSend) > (1/SENDRATE):
        server.sendData(b'A' ,struct.pack('4f', *r[0]))
        server.sendData(b'T' ,struct.pack('4f', *r[1]))
        lastSend += 1/SENDRATE


#--------------------SETUP--------------------
def setup():
    CL.log(CL.INFO, "Beginning setup")
    globalVars()

    print(PROPERTIES)

    if LOGGING:
        logger.setupFile(config)
    server.setup(config, [setInput])
    relativeMotion.setup(config)
    VGC.setup(config)
    if 'USE_GPIO' in PROPERTIES:
        GPIO.setup(config)
    if 'USE_VISUALIZER' in PROPERTIES:
        visualizer.setup(config)
    if 'USE_GPIO' in PROPERTIES:
        GPIO.setStatus(1)

    CL.log(CL.INFO, "setup is complete")


def globalVars():
    global startTime, lastSend, lastLog, IS_ACTIVE, light
    IS_ACTIVE = True
    startTime = time.time()
    lastSend = 0
    lastLog = 0
    light = 0


if __name__ == '__main__':
    setup()
    setInput((0, 0, 0), 0)
    CL.log(CL.INFO, "loop starting")
    while IS_ACTIVE:
        loop()
    CL.log(CL.INFO, "loop stopping")
    if USE_GPIO:
        GPIO.atexit()
