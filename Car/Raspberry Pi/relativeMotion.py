from math import *


def setup(config):
    global b, w
    w = float(config.get('car', 'width'))
    b = float(config.get('car', 'wheelbase')) / 2


def calcS(angle, pwr):
    angleL = 0
    angleR = 0
    pwrL = 1
    pwrR = 1
    if angle != 0:
        a1 = abs(angle)
        r1 = b / sin(a1)
        r2 = sqrt(pow((sqrt(r1*r1-b*b)+w),2) + b*b)
        a2 = asin(b/r2)

        right = (angle > 0)

        angleR = angle       if right else -a2
        angleL = a2 if right else angle

        pwrR = r1/r2 if right else 1
        pwrL = 1     if right else r1/r2

    return ((angleR, angleL, -angleR, -angleL), power(pwr, pwrR, pwrL, pwrR, pwrL))

def calcES(angle, pwr):
    angleB = -angle
    angleF = angle
    return ((angleF, angleF, -angleB, -angleB), (pwr, pwr, pwr, pwr))


def calcC(tcAngle, tcDist, pwr):
    angleFR = 0
    angleFL = 0
    angleBR = 0
    angleBL = 0
    pwrFR = -1
    pwrFL = -1
    pwrBR = -1
    pwrBL = -1

    if tcDist == inf:
        angleFR = tcAngle + pi/2
        angleFL = tcAngle + pi/2
        angleBR = tcAngle + pi/2
        angleBL = tcAngle + pi/2

    else:
        a = tcAngle
        x = tcDist * sin(a)
        y = tcDist * cos(a)

        rFR = hypot(w/2 - x, b-y)
        r = rFR
        rFL = hypot(-w/2 - x, b-y)
        if(rFL > r):
            r = rFL
        rBR = hypot(w/2 - x, -b-y)
        if(rBR > r):
            r = rBR
        rBL = hypot(-w/2 - x, -b-y)
        if(rBL > r):
            r = rBL

        pwrFR = -rFR / r
        pwrFL = rFL / r
        pwrBR = -rBR / r
        pwrBL = rBL / r

        angleFR = -pi/2 + (atan2(w/2 - x, b-y))
        angleFL = pi/2 + (atan2(-w/2 - x, b-y))
        angleBR = -pi/2 + (atan2(w/2 - x, -b-y))
        angleBL = pi/2 + (atan2(-w/2 - x, -b-y))

    if (angleFR > pi/2):
       angleFR = angleFR - pi
       pwrFR *= -1
    if (angleFL > pi/2):
        angleFL = angleFL - pi
        pwrFL *= -1
    if (angleBR > pi/2):
        angleBR = angleBR - pi
        pwrBR *= -1
    if (angleBL > pi/2):
        angleBL = angleBL - pi
        pwrBL *= -1
    if (angleFR < -pi/2):
        angleFR = pi + angleFR
        pwrFR *= -1
    if (angleFL < -pi/2):
        angleFL = pi + angleFL
        pwrFL *= -1
    if (angleBR < -pi/2):
        angleBR = pi + angleBR
        pwrBR *= -1
    if (angleBL < -pi/2):
        angleBL = pi + angleBL
        pwrBL *= -1


    return ((angleFR, angleFL, angleBR, angleBL), power(pwr, pwrFR, pwrFL, pwrBR, pwrBL))

def power(pwr, pwrFR, pwrFL, pwrBR, pwrBL):
    return (pwrFR * pwr, pwrFL * pwr, pwrBR * pwr, pwrBL * pwr)
