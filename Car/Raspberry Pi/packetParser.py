import struct
import routines
import imp

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
        else:
            CL.log(CL.ERROR, "Invalid identifier %s" % packetID)


def cbSimpleSteering(data):
    r = struct.unpack('ff', data[0:4*2])
    cbFunctions[0]((r[0], 0, r[1]), 0)
    return data[4*2:]


def cbComplexSteering(data):
    r = struct.unpack('fff', data[0:4*3])
    cbFunctions[0]((r[0], r[1], r[2]), 1)
    return data[4*3:]


def cbTowBar(data):
    r = struct.unpack('f', data[0:4*1])
    cbFunctions[4](3, r[0])
    return data[4*1:]


def cbRotation(data):
    r = struct.unpack('ff', data[0:4*2])
    vgc = VGC.calcVGC(r, 0)
    SE.sendData(b'V', struct.pack('ffff', *vgc))
    return data[4*2:]


def cbOptions(data):
    identifier = data[0:1]
    value = data[1]
    cbFunctions[1](identifier, value)
    return data[2:]


def cbVGCModeSelect(data):
    value = data[0:1]
    cbFunctions[3]('VGC Mode', value)
    return data[1:]


def cbRoutines(data):
    value = data[0]
    imp.reload(routines)
    routines.do(cbFunctions)
    return data[1:]


handlerFunctions = {
    b's': cbSimpleSteering,
    b'c': cbComplexSteering,
    b'b': cbTowBar,
    b't': cbOptions,
    b'R': cbRotation,
    b'v': cbVGCModeSelect,
    b'd': cbRoutines,
}
