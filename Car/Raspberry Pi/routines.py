import time
import consoleLog as CL

routine1 = [
(0.7, [( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0), (1, 1, 1, 1), 0.5, 0]),
(0.7, [(-1.57, -1.57, -1.57, -1.57), (0, 0, 0, 0), (1, 1, 1, 1), 0.5, 0]),
(1.4, [( 1.57,  1.57,  1.57,  1.57), (0, 0, 0, 0), (1, 1, 1, 1), 0.5, 0]),
(0.7, [( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0), (1, 1, 1, 1), 0.5, 0]),
]

def do(cbFunctions):
    executeRoutine(routine1, "Steering Demo", cbFunctions)

def executeRoutine(routine, routineName, cbFunctions):
    CL.log(CL.ROUTINE, "Starting routine: \"%s\"" % routineName)
    startTime = time.time()

    for i in range(len(routine)):
        cbFunctions[4](-1, routine[i][1])
        time.sleep(sleepTime)
