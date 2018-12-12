import consoleLog as CL

def setProperty(property, value):
    if property == b'L':
        CL.log(CL.INFO, "Light set to %s" % value)
    elif property == b'B':
        CL.log(CL.INFO, "Buzzer set to %s" % value)
    else:
        CL.log(CL.ERROR, "Property name not found: %s" % property)
