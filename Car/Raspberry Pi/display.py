from math import *
import webcolors


def createPolygons():
    global wheelCenters, wheelCoords, oldOffset
    global wheelPolygons, textObjects
    wheelCenters = [] #centers of the 4 adjustedWheels
    wheelCoords = [] #coords of the 4 adjustedWheel rectangles
    limitCoords = [] #coords of the 4 adjustedWheel rectangles
    wheelPolygons = [] #adjustedWheels
    textObjects = [] #text above adjustedWheels

    adjustedWheelW = wheelW * scl/2
    adjustedWheelH = wheelH * scl/2
    origin = (w/2, h/2)

    oldOffset = (0, 0)

    for i in range (4):
        isFront = (not (i >> 1))*2-1
        isRight = (not(i & 1))*2-1
        ce = (origin[0] + isRight*scl*width/2, origin[1] - isFront*scl*weelbase/2)
        wheelCenters.append(ce)
        c.create_line(origin[0], origin[1], ce[0], ce[1], fill='white', width = 2)

        ce = (ce[0] + wheelOffset * isRight * scl, ce[1])

        xy = [(ce[0]-adjustedWheelW, ce[1]-adjustedWheelH), (ce[0]+adjustedWheelW, ce[1]-adjustedWheelH), (ce[0]+adjustedWheelW, ce[1]+adjustedWheelH), (ce[0]-adjustedWheelW, ce[1]+adjustedWheelH)]
        wheelCoords.append(xy)

        wheelPolygons.append(c.create_polygon(xy, fill='', outline='black'))
        textObjects.append(c.create_text(ce[0], ce[1]+adjustedWheelH+10, text='0', fill='white'))
    textObjects.append(c.create_text(w/2, 10, text='0', fill='white'))


def update(r, msg):
    ret = []
    for i in range(0, 4):
        a = r[0][i]
        ret.append(complex(cos(a), sin(a)))
        c.itemconfig(textObjects[i], text="%d, %04.2f" %(r[0][i], r[1][i]))

        value = floor(abs(r[1][i]) * 256)
        c.itemconfig(wheelPolygons[i], outline=getHex(value))

    c.itemconfig(textObjects[4], text=msg)
    rotatePolygons(ret)


def rotatePolygons(angles):
    for i in range(4):
        wheelOffsetD = wheelOffset
        if (wheelCenters[i][0] < 0):
            wheelOffsetD *= -1
        offsetO = complex(wheelCenters[i][0] + wheelOffsetD, wheelCenters[i][1])
        offsetN = complex(wheelCenters[i][0] + wheelOffsetD, wheelCenters[i][1])

        newxy = []
        for x, y in wheelCoords[i]:
            v = angles[i] * (complex(x, y) - offsetO) + offsetN
            newxy.append(v.real)
            newxy.append(v.imag)
        c.coords(wheelPolygons[i], *newxy)


def setup(_width, _wheelbase, wheelWidth, wheelDiameter, _wheelOffset, canvas, cW, cH, scale):
    global width, weelbase, c, w, h, scl, wheelH, wheelW, wheelOffset
    scl = scale
    width = _width
    weelbase = _wheelbase
    wheelH = wheelDiameter
    wheelW = wheelWidth
    wheelOffset = _wheelOffset
    c = canvas
    w = cW
    h = cH

    createPolygons()


def getHex(value):
        return webcolors.rgb_to_hex((value, value, value))
