from tkinter import *
import display as di
from math import *


def setup(config):
    global canvasWidth, canvasHeight, canvasScale, width, wheelbase, wheelWidth, wheelDiameter, wheelOffset
    canvasWidth = int(config.get('display', 'width'))
    canvasHeight = int(config.get('display', 'height'))
    canvasScale = float(config.get('display', 'scale'))
    width = float(config.get('car', 'width'))
    wheelbase = float(config.get('car', 'wheelbase'))
    wheelWidth = float(config.get('car', 'wheelWidth'))
    wheelDiameter = float(config.get('car', 'wheelDiameter'))
    wheelOffset = float(config.get('car', 'wheelOffset'))

    global root, angleText
    root = Tk()
    setupCanvas()
    angleText = "no vi input"


def setInput(r, light):
    msg = "angle: %s°; light is %s" % (angleText, "on" if light else "off")
    di.update(r, msg)

def update():
    canvas.pack()
    root.update()


def getInput():
    dx = root.winfo_pointerx() - root.winfo_rootx() - origin[0]
    dy = root.winfo_pointery() - root.winfo_rooty() - origin[1]
    dx /= canvasScale
    dy /= -canvasScale

    angle = atan2(dx, dy)
    l = hypot (dx, dy)

    global angleText
    angleText = "%d"%(degrees(angle))

    return (angle, l, 1)


def setupCanvas():
    global canvas, origin
    origin = (canvasWidth / 2, canvasHeight / 2)
    canvas = Canvas(width=canvasWidth, height=canvasHeight)
    canvas.pack()
    canvas.configure(background=di.getHex(51))
    di.setup(width, wheelbase, wheelWidth, wheelDiameter, wheelOffset, canvas, canvasWidth, canvasHeight, canvasScale)
