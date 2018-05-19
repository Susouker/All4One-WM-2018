import socket
import time
from threading import Thread
import consoleLog as CL

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
                CL.log(CL.SERVERMSG, "(%s) Reveived %s" % (self.addr[0], r.decode()))
                r = r.split(b'$')
                for msg in r:
                    if msg != b'':
                        receiveData(msg[:1], msg[1:])

            except ConnectionResetError:
                CL.log(CL.ERROR, "Connection Reset")
                break

        self.conn.close()
        CL.log(CL.SERVER, "(%s) Client disconnected" % self.addr[0])
        global conns
        conns.remove(self.conn)


class SocketHandler(Thread):
    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.bind((HOSTNAME, PORT))
            CL.log(CL.SERVER, "Bind was succesful")
        except socket.error as msg:
            CL.log(CL.ERROR, "Bind failed; " + str(msg))
            return

        self.s.listen()
        while 1:
            (conn, addr) = self.s.accept()
            global conns
            conns.append(conn)

            connHandler = ConnHandler(conn, addr)
            connHandler.setDaemon(True)
            connHandler.start()
            CL.log(CL.SERVER, "(%s) Client connected; Total number of connections is %s" % (addr[0], len(conns)))


def receiveData(type, data):
    CL.log(CL.SERVERMSG, "Received: %s; %s" % (type, data))
    global callbacks
    try:
        callbacks[type](data)
    except KeyError:
        CL.log(CL.ERROR, "Invalid identifier %s" % type)


def sendData(type, data):
    CL.log(CL.SERVERMSG, "Sending: %s; %s" % (type, data))
    msg = b'$' + type + data
    for conn in conns:
        try:
            conn.send(msg)
        except:
            CL.log(CL.ERROR, "Send failed")
