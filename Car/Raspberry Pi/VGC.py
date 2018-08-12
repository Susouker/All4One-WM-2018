from math import *

mode = 0 #0=flat 1=hillclimb 2=tilted 3=articulation

width = 0.15
wheelbase = 0.3
MAX = .07

def setup(config):
    global MAX, width, wheelbase
    MAX = float(config.get('car', 'VGCMax'))
    width = float(config.get('car', 'width'))
    wheelbase = float(config.get('car', 'wheelbase'))


def setMode(m):
    mode = m


def calcVGC(rotation, current):
    if mode == 0:
        calcVGCSimple(rotation, current)
    else if mode == 1:
        calcVGCFlat()

def calcVGCFlat():
    return (0, 0, 0, 0)

def calcVGCSimple(rotation, current):
    slope = (rotation[0], rotation[1]) #implement current
    print(slope)

    diff = ((tan(radians(slope[0]))*wheelbase), (tan(radians(slope[1]))*width))

    FR = MAX
    FL = MAX
    BR = MAX
    BL = MAX

    v1 = diff[0]
    if diff[0] > 0:
        FR -= v1
        FL -= v1
    else:
        BR += v1
        BL += v1

    v2 = diff[1]
    if diff[1] > 0:
        FR -= v2
        BR -= v2
    else:
        FL += v2
        BL += v2

    return (max(FR, 0), max(FL, 0), max(BR,0), max(BL,0))
