from math import *
import consoleLog as CL

mode = 0

width = 0.15
wheelbase = 0.3

def setup(config):
    global MAX, width, wheelbase
    width = float(config.get('car', 'width'))
    wheelbase = float(config.get('car', 'wheelbase'))


def setMode(m):
    CL.log(CL.VGC, "Mode set to %s" % m)
    mode = m


def calcVGC(time):
    if mode == b'P':
        calcVGCHigh()
    elif mode == b'A':
        calcVGCArti(time)
    else #if mode == b'F':
        calcVGCFlat()

def calcVGCFlat():
    return [0, 0, 0, 0]

def calcVGCHigh():
    return [1, 1, 1, 1]

def calcVGCArti(time):
    return [(time) % 2, (time + 1) % 2, (time + 1) % 2, (time) % 2]
