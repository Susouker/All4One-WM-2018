import time


def setupFile(config):
    timeStr = time.strftime("%y%m%d%H%M%S", time.localtime())
    
    global logFileURL
    logFileURL = config.get('app', 'logfile')
    logFileURL = logFileURL % (timeStr)
    with open(logFileURL, "w") as file:
        file.write("sep=,\n")
        file.write(timeStr)
        file.write("Time,Lights,input0,input1,input2,"
                   +"angleFR,angleFL,angleBR,angleBL,powerFR,powerFL,powerBR,powerBL")
    
def log(*args):
    msg = ""
    for arg in args:
        msg += str(arg) + ','
    msg = msg[:-1]
    msg = msg.translate({ord(c): None for c in ' ()'})
    
    with open(logFileURL, "a") as file:
        file.write("\n" + msg)