from tkinter import *
import display as di
from math import *


def setup(config, _cbFunctions):
    global canvasWidth, canvasHeight, canvasScale, width, wheelbase, wheelWidth, wheelDiameter, wheelOffset, cbFunctions
    cbFunctions = _cbFunctions
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


def setInput(r):
    di.update(r, angleText)

def update():
    canvas.pack()
    root.update()


def getInput():
    dx = root.winfo_pointerx() - root.winfo_rootx() - origin[0]
    dy = root.winfo_pointery() - root.winfo_rooty() - origin[1]
    dx /= canvasScale
    dy /= -canvasScale

    mode = 4
    if dy > 0.1:
        mode = 7
    elif dy < -0.1:
        mode = 6
    #cbFunctions[0](mode)

    global angleText
    angleText = "%f, %f"%(dx, dy)


    return (dx, 1)


def setupCanvas():
    global canvas, origin
    origin = (canvasWidth / 2, canvasHeight / 2)
    canvas = Canvas(width=canvasWidth, height=canvasHeight)
    canvas.pack()
    canvas.configure(background=di.getHex(51))
    di.setup(width, wheelbase, wheelWidth, wheelDiameter, wheelOffset, canvas, canvasWidth, canvasHeight, canvasScale)
