from math import *

mode = 20

def setup(config, _cbFunctions):
    global cbFunctions, b, w, maxAngle, swfost
    cbFunctions = _cbFunctions
    w = float(config.get('car', 'width')) / 2
    b = float(config.get('car', 'wheelbase')) / 2
    swfost = int(config.get('control', 'steeringWheelForOnSpotTurning'))

def setMode(m):
    global mode
    mode = int(m)
    sendMode()
    cbFunctions[1](0, 0)

def sendMode():
    cbFunctions[0]('M', chr(mode))


def calc(angle, pwr):
    pwr = min(max(pwr, -1), 1)
    angle = min(max(angle, -pi/4), pi/4)

    if mode == 0:                       # Full
        return fullCalc(angle[0], angle[1], pwr)

    elif mode == 20:                    # Seitwärts
        return ([angle]*4, [pwr]*4)
    elif mode == 21:                    # Seitwärts
        if swfost:
            pwr = angle * 4/pi
        return ([2*pi/6, -2*pi/6, -2*pi/6, 2*pi/6], [pwr, -pwr, -pwr, pwr])

    elif mode == 28:                    # Auf der Stelle
        if swfost:
            pwr = angle * 4/pi
        return fullCalc(0, 0, angle * 4/pi)

    if angle == 0:                      # geradeaus
        return ([0] * 4, [pwr] * 4)

                                        # normal
    isRight = 1
    if angle < 0:
        isRight = -1
        angle = -angle

    centerY = 0
    if mode == 6:
        centerY = -b
    elif mode == 7:
        centerY = b
    centerX = ((b + abs(centerY)) / tan(angle) + w) * isRight
    return fullCalc(centerX, centerY, pwr)


def fullCalc(centerX, centerY, pwr):
    maxRadius = 0
    radii = [0,0,0,0]
    xPos = [0,0,0,0]
    yPos = [0,0,0,0]
    angles = [0,0,0,0]
    pwrs = [0,0,0,0]
    flip = centerX > -w and centerX < w

    for i in range(4):
        isFront = (not (i >> 1))*2-1
        isRight = (i & 1)*2-1
        xPos[i] = w * isRight - centerX
        yPos[i] = b * isFront - centerY
        radii[i] = hypot(xPos[i], yPos[i])
        maxRadius = max(maxRadius, radii[i])

        if xPos[i] == 0:
            angles[i] = 0  # sollte eig nicht vorkommen, aber man weiß ja nie
        else:
            angles[i] = atan(- yPos[i] / xPos[i])
            if isRight:
                angles[i] = min(max(angles[i], -2*pi/6), pi/4)
            else:
                angles[i] = min(max(angles[i], -pi/4), 2*pi/6)

    for i in range(4):
        pwrs[i] = radii[i] / maxRadius * pwr
        if flip and i & 1:
            pwrs[i] = -pwrs[i]

    return (angles, pwrs)
