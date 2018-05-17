USE_VI = True
INPUT = 0 #0VI 1TCP
LOGGING = True
FRAMERATE = 15
SENDRATE = 0.01
LOGRATE = 5
CONFIG_URL = "config.conf"

import relativeMotion as RM
import VGC
if USE_VI:
    import visualizer as VI
import i2cManager as I2C
import gpioManager as GPIO
if LOGGING:
    import logger as LO
import consoleLog as CL
import server as SE

from math import *
import configparser
import time

IS_ACTIVE = True
compMode = 0 #1=competition
steeringMode = 1 #0Simple 1Complex
buzz = False


def loop():
    global startTime, lastTime, lastSend, lastLog

    currentTime = time.time() - startTime
    deltaTime = currentTime - lastTime
    if deltaTime < (1/FRAMERATE):
        return
    lastTime = currentTime

    #Get input from Mouse Curosr if vi is used
    if INPUT == 0 and USE_VI:
        try:
            input = VI.getInput()
        except:
            global IS_ACTIVE
            IS_ACTIVE = False
            return
    elif INPUT == 1:
        global throttle, steering
        input = (steering[0], steering[1], throttle)
    else:
        input = (0, 0, 0)


    #12c Stuff
    light = I2C.readLightSensor()[0]
    if buzz:
        I2C.setBuzzer(False)

    #Calculate RM based on input
    r = RM.calcC(input[0], input[1], input[2]) if steeringMode == 1 else RM.calcS(input[0], input[2])

    #Update
    if USE_VI:
       VI.update(r, light)

    #Log data
    if LOGGING and (currentTime - lastLog) > (1/LOGRATE):
        LO.log(currentTime, light, input, r)
        lastLog += 1/LOGRATE

    #Send Data over TCP
    if (currentTime - lastSend) > (1/SENDRATE):
        SE.sendData(r[0], "A")
        SE.sendData(r[1], "P")
        lastSend += 1/SENDRATE

    #except:
     #   global IS_ACTIVE
      #  IS_ACTIVE = False
       # cl.log(cl.INFO, "Stoppping app because of an error")

def setup():
    CL.log(CL.INFO, "Beginning setup")
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_URL)
        CL.log(CL.INFO, "Config file read")
    except:
        CL.log(CL.ERROR, "while loading config")

    global startTime, lastTime, lastSend, lastLog, throttle, steering
    startTime = time.time()
    lastTime = 0
    lastSend = 0
    lastLog = 0
    throttle = 0
    steering = (0, 0)

    if LOGGING:
        LO.setupFile(config)
        CL.log(CL.INFO, "Log file has been created")

    SE.setup(config, {"S":cbS, "T":cbT, "R":cbR, "M":cbM})
    CL.log(CL.INFO, "server is setup")

    RM.setup(config)
    VGC.setup(config)
    GPIO.setup(config)
    CL.log(CL.INFO, "rm, vgc and gpio are setup")

    if USE_VI:
        VI.setup(config)
        CL.log(CL.INFO, "Visualization is setup")

    CL.log(CL.INFO, "setup is complete")
    GPIO.setStatus(1)


def setCompetitionMode(b):
    compMode = 1 if b else 0
    GPIO.setMode(b)
    if b:
        I2C.setLightmode(True, True)
        buzz = True

def cbS(vals):
    global steering
    steering = vals
def cbT(vals):
    global thottle
    throttle = vals[0]
def cbR(vals):
    vgc = VGC.calcVGC(toFloatArray(vals), 0)
    SE.sendData(vgc, "V")
def cbM(vals):
    return

def toFloatArray(vals):
    r = []
    for val in vals:
        r.append(float(val))
    return r


setup()
CL.log(CL.INFO, "loop starting")
while IS_ACTIVE:
    loop()
CL.log(CL.INFO, "loop stopping")
GPIO.atexit()
