import socket
import time
import struct
from threading import Thread
from tkinter import *
from math import *

PORT = 14044
HOST = '192.168.178.48'
SENDRATE = 10
canvasWidth = 640
canvasHeight = 360
scl = 300

def receiveData(data):
    print ("Received: %s" % (data))


def sendData(packetID, data):
    lastSend = time.time()
    print ("Sending: %s; %s" % (packetID, data))
    msg = packetID + data
    client.send(msg)


class SocketHandler(Thread):
    def run(self):
        while 1:
            try:
                r = self.conn.recv(1024)
                #CL.log(CL.SERVERMSG, "(%s) Reveived %s" % (self.addr[0], r.decode()))
                receiveData(r)
            except ConnectionResetError:
                print ("connection closed")
                break

def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("trying to connect")
    try:
        client.connect((HOST, PORT))
    except TimeoutError:
        print("connection timed out")
        return
    except ConnectionRefusedError:
        print("connection refused")
        return
    print ("connected")

    socketHandler = SocketHandler()
    socketHandler.setDaemon(True)
    socketHandler.start()


def setupCanvas():
    global canvas, center, line, lastSend
    center = (canvasWidth/2, canvasHeight)
    canvas = Canvas(width=canvasWidth, height=canvasHeight)
    line = canvas.create_line((0,0,0,0), fill="white", width=3)
    drawOvals()
    canvas.pack()
    canvas.configure(background="#282c34")
    canvas.bind("<B1-Motion>", motion)
    lastSend = time.time()
def drawOvals():
    n = 4
    for i in range(1, n+1):
        canvas.create_oval(center[0]-scl/n*i, center[1]-scl/n*i, center[0]+scl/n*i, center[1]+scl/n*i, outline="white", width=2)

def motion(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.coords(line, (*center, x, y))
    dx = x - center[0]
    dy = y - center[1]
    angle = degrees(atan2(dy, dx)) + 90
    lenght = min(hypot(dx, dy) / scl, 1)
    if(lenght < 0.05):
        lenght = 0

    #Send Data over TCP
    global lastSend
    if (time.time() - lastSend) > (1/SENDRATE):
        sendData(b'e', struct.pack('2f', angle, lenght))
        print ("%s, %s" % (angle, lenght))
        lastSend = time.time()



connect()

setupCanvas()
mainloop()

print ("closing socket")
client.close()
