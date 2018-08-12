import struct

SOCKET_AS_INPUT = 1

def setup(config, _cbFunctions):
    global cbFunctions
    cbFunctions = _cbFunctions

def parse(data):
    while len(data) > 0:
        packetID = data[:1]
        if packetID in handlerFunctions:
            data = handlerFunctions[packetID](data[1:])
        else:
            CL.log(CL.ERROR, "Invalid identifier %s" % packetID)

def cbExtraSimpleSteering(data):
    if(SOCKET_AS_INPUT):
        r = struct.unpack('ff', data[0:4*2])
        cbFunctions[0]((r[0], 0, r[1]), -1)
    return data[4*2:]

def cbSimpleSteering(data):
    if(SOCKET_AS_INPUT):
        r = struct.unpack('ff', data[0:4*2])
        cbFunctions[0]((r[0], 0, r[1]), 0)
    return data[4*2:]

def cbComplexSteering(data):
    if(SOCKET_AS_INPUT):
        r = struct.unpack('fff', data[0:4*3])
        cbFunctions[0]((r[0], r[1], r[2]), 1)
    return data[4*3:]

def cbRotation(data):
    r = struct.unpack('ff', data[0:4*2])
    vgc = VGC.calcVGC(r, 0)
    SE.sendData(b'V', struct.pack('ffff', *vgc))
    return data[4*2:]

def cbOptions(data):
    identifier = data[0:1]
    value = data[1]
    if (identifier == b'L'):
        cbFunctions[1]('Light', value)
    if (identifier == b'B'):
        d = 1

    return data[2:]

def cbVGCModeSelect(data):
    value = data[0]
    cbFunctions[1]('VGC Mode', value)
    return data[1:]

def cbRoutinen(data):
    value = data[0]
    #TODO führe Routine aus
    return data[1:]

handlerFunctions = {
    b's': cbSimpleSteering,
    b'c': cbComplexSteering,
    b't': cbOptions,
    b'R': cbRotation,
    b'e': cbExtraSimpleSteering,
    b'v': cbVGCModeSelect,
    b'd': cbRoutinen,
}
