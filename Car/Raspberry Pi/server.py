import socket
import time
from threading import Thread
import consoleLog as cl
import struct
from array import array

conns = []

def setup(config, callbackFunctions):
    global callbacks, PORT, HOSTNAME
    callbacks = callbackFunctions
    PORT = int(config.get('server', 'port'))
    HOSTNAME = config.get('server', 'hostname')
    
    socketHandler = SocketHandler()
    socketHandler.setDaemon(True)
    socketHandler.start()


class ConnHandler(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        while 1:
            try:
                r = self.conn.recv(1024)
                if r == b'':
                    break
                cl.log(cl.SERVERMSG, "(%s) Reveived %s" % (self.addr[0], r.decode("utf8")))
                
                msg = r.decode("utf-8").split('!')
                for s in msg:
                    if s != '':
                        receiveData(s[1:], s[:1])
                
            except ConnectionResetError:
                cl.log(cl.ERROR, "In conn recv")
                break
        
        self.conn.close()
        cl.log(cl.SERVER, "(%s) Client disconnected" % self.addr[0])
        global conns
        conns.remove(self.conn)


class SocketHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.bind((HOSTNAME, PORT))
            cl.log(cl.SERVER, "Bind was succesful")
        except socket.error as msg:
            cl.log(cl.ERROR, "Bind failed; " + str(msg))
            return

        self.s.listen(5)
        connections = 0
        SocketHandler
        while 1:
            (conn, addr) = self.s.accept()
            global conns
            conns.append(conn)
            
            connHandler = ConnHandler(conn, addr)
            connHandler.setDaemon(True)
            connHandler.start()
            
            cl.log(cl.SERVER, "(%s) Client connected; Total number of connections is %s" % (addr[0], len(conns)))


def receiveData(data, type):
    cl.log(cl.SERVERMSG, "Received: %s; %s" % (type, data))
    
    global callbacks
    callbacks[type](data.split(','))


def sendData(data, type):
    data = str(data).translate({ord(c): None for c in ' ()'})
    cl.log(cl.SERVERMSG, "Sending: %s; %s" % (type, data))
    
    s = "!" + type + data
    s = s.encode()
    for conn in conns:
        try:
            conn.send(s)
        except:
            cl.log(cl.ERROR, "Send failed")
