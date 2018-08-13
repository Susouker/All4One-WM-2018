import time
import consoleLog as CL

routine1 = (
(0.7, (( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0))),
(1.4, ((-1.57, -1.57, -1.57, -1.57), (0, 0, 0, 0))),
(2.8, (( 1.57,  1.57,  1.57,  1.57), (0, 0, 0, 0))),
(3.4, (( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0))),
)

def do(cbFunctions):
    executeRoutine(routine1, "Steering Demo", cbFunctions)

def executeRoutine(routine, routineName, cbFunctions):
    CL.log(CL.ROUTINE, "Starting routine \"%s\"" % routineName)
    startTime = time.time()

    for i in range(len(routine)):
        if i > 0:
            curR = routine[i - 1][1]
        else:
            curR = cbFunctions[2]()

        timeOfAction = routine[i][0] + startTime
        timeForAction = timeOfAction - time.time()

        nxtR = routine[i][1]
        while time.time() < timeOfAction:
            p = 1 - ((timeOfAction - time.time() ) / timeForAction)
            cbFunctions[0](LERPr(curR, nxtR, p), -4)


def waitUntil(timeToWaitFor):
    sleepTime = timeToWaitFor - time.time()
    if sleepTime > 0:
        time.sleep(sleepTime)

def LERPr(cur, nxt, p):
    result = ([0, 0, 0, 0], cur[1])
    for i in range(4):
        result[0][i] = cur[0][i] + (nxt[0][i] - cur[0][i]) * p
    return result
