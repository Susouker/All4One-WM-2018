USE_VI = True #wether or not to display the visualization
USE_I2C = False #wether or not to use i2c
USE_GPIO = False #wether or not to use the gpio output
INPUT = 'V' #V to use the visualization as input
LOGGING = False
FRAMERATE = 15
SENDRATE = 0.05
LOGRATE = 5
CONFIG_URL = "config.conf"

import relativeMotion as RM
import VGC
if USE_VI:
    import visualizer as VI
if USE_I2C:
    import i2cManager as I2C
if USE_GPIO:
    import gpioManager as GPIO
if LOGGING:
    import logger as LO
import consoleLog as CL
import server as SE

from math import *
import configparser
import struct
import time

IS_ACTIVE = True
compMode = 0 #1=competition
steeringMode = 1 #0Simple 1Complex
buzz = False


#--------------------LOOP--------------------
def loop():
    global startTime, lastTime, lastSend, lastLog

    currentTime = time.time() - startTime
    deltaTime = currentTime - lastTime
    if deltaTime < (1/FRAMERATE):
        return
    lastTime = currentTime

    #Get input from Mouse Curosr if vi is used
    global input
    if INPUT == 'V' and USE_VI:
        try:
            input = VI.getInput()
        except:
            global IS_ACTIVE
            IS_ACTIVE = False
            return

    #12c Stuff
    if USE_I2C:
        light = I2C.readLightSensor()[0]
        if buzz:
            I2C.setBuzzer(False)
    else:
        light = 0

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
        SE.sendData(b'A' ,struct.pack('4f', *r[0]))
        SE.sendData(b'T' ,struct.pack('4f', *r[1]))
        lastSend += 1/SENDRATE


#--------------------SETUP--------------------
def setup():
    CL.log(CL.INFO, "Beginning setup")
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_URL)
        CL.log(CL.INFO, "Config file read")
    except:
        CL.log(CL.ERROR, "while loading config")

    globalVars()

    if LOGGING:
        LO.setupFile(config)
        CL.log(CL.INFO, "Log file has been created")

    SE.setup(config, {b's':cbSimpleSteering, b'c':cbComplexSteering, b'r':cbR})
    CL.log(CL.INFO, "server is setup")

    RM.setup(config)
    VGC.setup(config)
    if USE_GPIO:
        GPIO.setup(config)
    CL.log(CL.INFO, "rm, vgc and gpio are setup")

    if USE_VI:
        VI.setup(config)
        CL.log(CL.INFO, "Visualization is setup")

    CL.log(CL.INFO, "setup is complete")
    if USE_GPIO:
        GPIO.setStatus(1)

def globalVars():
    global startTime, lastTime, lastSend, lastLog, input
    startTime = time.time()
    lastTime = 0
    lastSend = 0
    lastLog = 0
    input = (0, 0, 0)


#--------------------|--------------------
def setCompetitionMode(b):
    compMode = 1 if b else 0
    if USE_GPIO:
        GPIO.setMode(b)
    if b:
        if USE_I2C:
            I2C.setLightmode(True, True)
        buzz = True


#--------------------CALLBACKS--------------------
def cbSimpleSteering(vals):
    if len(vals) == 8: #2 float á 4 bytes
        global input, steeringMode
        steeringMode = 0
        r = struct.unpack('2f', vals)
        input = (r[0], 0, r[1])
def cbComplexSteering(vals):
    if len(vals) == 12: #2 float á 4 bytes
        global input, steeringMode
        steeringMode = 1
        r = struct.unpack('3f', vals)
        input = (r[0], r[1], r[2])
def cbR(vals):
    if len(vals) == 8: #2 floats á 4 bytes
        vgc = VGC.calcVGC(struct.unpack('2f', vals), 0)
        SE.sendData(b'V', struct.pack('4f', *vgc))


#--------------------MAIN--------------------
setup()
CL.log(CL.INFO, "loop starting")
while IS_ACTIVE:
    loop()
CL.log(CL.INFO, "loop stopping")
if USE_GPIO:
    GPIO.atexit()
