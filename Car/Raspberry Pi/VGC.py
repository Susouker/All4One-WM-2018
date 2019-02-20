from math import *
import consoleLog as CL

mode = b'P'
height = 0

width = 0.15
wheelbase = 0.3

def setup(config):
    global MAX, width, wheelbase
    width = float(config.get('car', 'width'))
    wheelbase = float(config.get('car', 'wheelbase'))


def setMode(m, h):
    global mode, height
    CL.log(CL.VGC, "Mode set to %s" % m)
    mode = m
    height = h


def calcVGC(time):
    if mode == b'P':
        return [1]*4
    elif mode == b'A':
        return calcVGCArti(time)
    elif mode == b'M':
        return [height]*4
    else: #if mode == b'F':
        return [0]*4

def calcVGCArti(time):
    return ((time) % 2, (time + 1) % 2, (time + 1) % 2, (time) % 2)
