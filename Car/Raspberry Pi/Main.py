CONFIG_URL = "config.conf"
timeDelta = 0.04

#--------------------INITIALSETUP--------------------
if __name__ == '__main__':
    from math import *
    import struct
    import time
    import consoleLog as CL
    import configparser
    from tkinter import TclError

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
        global IS_ACTIVE, outputChanged, forceOutput, nextTime
        t = time.time() - startTime

        if t > nextTime:
            CL.log(CL.ERROR, "%d ms skipped" % ((t - nextTime) * 1000))
            nextTime = t
        while t < nextTime:
            t = time.time() - startTime
        nextTime += timeDelta

        setCarOutput(2, VGC.calcVGC(t))

        #Get input from Mouse Curosr if visualizer is used
        if 'VISUALIZER_AS_INPUT' in PROPERTIES:
            setInput(*visualizer.getInput())

        if 'USE_GPIO' in PROPERTIES:
            if outputChanged or forceOutput < 4:
                carOutputManager.setCarOutput('P', carOutput, forceOutput)
            forceOutput += 1
            if forceOutput > 1 / timeDelta:
                forceOutput = 0

        if outputChanged:
            outputChanged = 0
            if 'USE_VISUALIZER' in PROPERTIES:
                visualizer.setInput(carOutput)

        #Update
        if 'USE_VISUALIZER' in PROPERTIES:
            visualizer.update()
        if 'USE_GPIO' in PROPERTIES:
            GPIO.update(t)

    except (KeyboardInterrupt, TclError):
        IS_ACTIVE = False
        return

def getCarOutput():
    return carOutput

def setCarOutput(category, value):
    global carOutput, outputChanged
    carOutput[category] = value
    outputChanged = True

def setInput(angle, pwr):
    r = relativeMotion.calc(angle, pwr)

    setCarOutput(0, r[0])
    setCarOutput(1, r[1])


#--------------------SETUP--------------------
def setup():
    CL.log(CL.INFO, "Beginning setup")
    globalVars()

    server.setup(config, [setInput, optionManager.setProperty, getCarOutput, VGC.setMode, setCarOutput, relativeMotion.setMode, sendAll])
    relativeMotion.setup(config, [server.sendData, setInput])
    VGC.setup(config)
    if 'USE_GPIO' in PROPERTIES:
        GPIO.setup(config)
        carOutputManager.setup(config)
    if 'USE_VISUALIZER' in PROPERTIES:
        visualizer.setup(config, [relativeMotion.setMode])

    CL.log(CL.INFO, "setup is complete")


def globalVars():
    global IS_ACTIVE, carOutput, startTime, forceOutput, nextTime
    IS_ACTIVE = True
    carOutput = [
    (0,0,0,0),  # Lenkwinkel
    (0,0,0,0),  # Throttle
    (1,1,1,1),  # VGC
    0.5]          # Tow Bar
    startTime = time.time()
    forceOutput = 0
    nextTime = 0

def sendAll():
    relativeMotion.sendMode()


if __name__ == '__main__':
    setup()
    setInput(0, 0)
    CL.log(CL.INFO, "loop starting")
    while IS_ACTIVE:
        loop()
    CL.log(CL.INFO, "loop stopping")
    if 'USE_GPIO' in PROPERTIES:
        GPIO.atexit()
