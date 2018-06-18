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
        a1 = radians(abs(angle))
        r1 = b / sin(a1)
        r2 = sqrt(pow((sqrt(r1*r1-b*b)+w),2) + b*b)
        a2 = asin(b/r2)

        right = (angle > 0)

        angleR = angle       if right else -degrees(a2)
        angleL = degrees(a2) if right else angle

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
        angleFR = tcAngle+90
        angleFL = tcAngle+90
        angleBR = tcAngle+90
        angleBL = tcAngle+90

    else:
        a = radians(tcAngle)
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

        angleFR = -90 + degrees(atan2(w/2 - x, b-y))
        angleFL = 90 + degrees(atan2(-w/2 - x, b-y))
        angleBR = -90 + degrees(atan2(w/2 - x, -b-y))
        angleBL = 90 + degrees(atan2(-w/2 - x, -b-y))

    if (angleFR > 90):
       angleFR = angleFR - 180
       pwrFR *= -1
    if (angleFL > 90):
        angleFL = angleFL - 180
        pwrFL *= -1
    if (angleBR > 90):
        angleBR = angleBR - 180
        pwrBR *= -1
    if (angleBL > 90):
        angleBL = angleBL - 180
        pwrBL *= -1
    if (angleFR < -90):
        angleFR = 180 + angleFR
        pwrFR *= -1
    if (angleFL < -90):
        angleFL = 180 + angleFL
        pwrFL *= -1
    if (angleBR < -90):
        angleBR = 180 + angleBR
        pwrBR *= -1
    if (angleBL < -90):
        angleBL = 180 + angleBL
        pwrBL *= -1


    return ((angleFR, angleFL, angleBR, angleBL), power(pwr, pwrFR, pwrFL, pwrBR, pwrBL))

def power(pwr, pwrFR, pwrFL, pwrBR, pwrBL):
    return (pwrFR * pwr, pwrFL * pwr, pwrBR * pwr, pwrBL * pwr)
