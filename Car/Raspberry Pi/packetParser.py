import struct
import routines
import imp
import consoleLog as CL

def setup(config, _cbFunctions):
    global cbFunctions
    cbFunctions = _cbFunctions


def parse(data):
    while len(data) > 0:
        packetID = data[:1]
        if packetID in handlerFunctions:
            try:
                data = handlerFunctions[packetID](data[1:])
            except struct.error:
                CL.log(CL.ERROR, "Invalid packet %s" % packetID)
            except InvalidPacketException:
                CL.log(CL.ERROR, "Invalid packet %s" % packetID)
        else:
            CL.log(CL.ERROR, "Invalid identifier %s" % packetID)
            data = data[1:]


def cbSteering(data):
    if len(data) < 2:
        raise InvalidPacketException
    cbFunctions[0]((data[0] * 0.00625) - 0.8, (data[1] / 128) - 1)
    return data[2:]


def cbTowBar(data):
    if len(data) < 4:
        raise InvalidPacketException
    r = struct.unpack('f', data[0:4*1])
    cbFunctions[4](3, r[0])
    return data[4*1:]


def cbSteeringMode(data):
    if len(data) < 1:
        raise InvalidPacketException
    cbFunctions[5](data[0])
    return data[1:]

def cbVGCMode(data):
    if len(data) < 1:
        raise InvalidPacketException
    mode = data[:1]
    if mode == b'M':
        cbFunctions[3](b'M', data[1] / 256)
        return data[2:]
    else:
        cbFunctions[3](mode, 0)
        return data[1:]

def cbSetReverse(data):
    if len(data) < 1:
        raise InvalidPacketException
    cbFunctions[7](data[0])
    return data[1:]

def cbVGCadjust(data):
    if len(data) < 1:
        raise InvalidPacketException
    cbFunctions[8](data[0])
    return data[1:]


def cbRoutines(data):
    if len(data) < 1:
        raise InvalidPacketException
    value = data[0]
    imp.reload(routines)
    routines.do(cbFunctions)
    return data[1:]


handlerFunctions = {
    b's': cbSteering,
    b'b': cbTowBar,
    b'd': cbRoutines,
    b'M': cbSteeringMode,
    b'H': cbVGCMode,
    b'Q': cbSetReverse,
    b'W': cbVGCadjust,
}

class InvalidPacketException(Exception):
    pass
