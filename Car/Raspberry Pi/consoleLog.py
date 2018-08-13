INFO = ("[INFO]", True)
ERROR = ("[ERROR]", True)
CB = ("[CALLBACK]", True)
VGC = ("[VGC]", True)
SERVER = ("[SERVER]", True)
SERVERMSG = ("[SERVER]", True)
ROUTINE = ("[ROUTINE]", True)

lastError = ""

def log(type, msg):
    if type[1]:
        if type == ERROR:
            global lastError
            if msg == lastError:
                return
            lastError = msg
        print(type[0] + ": " + msg)
