import time
import consoleLog as CL

routine1 = (
(0.0, (( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0))),
(0.7, ((-1.57, -1.57, -1.57, -1.57), (0, 0, 0, 0))),
(2.1, (( 1.57,  1.57,  1.57,  1.57), (0, 0, 0, 0))),
(2.8, (( 0   ,  0   ,  0   ,  0   ), (0, 0, 0, 0))),
)

def do(cbFunctions):
    executeRoutine(routine1, cbFunctions)

def executeRoutine(routine, cbFunctions):
    CL.log(CL.INFO, "starting routine")
    startTime = time.time()

    for i in range(len(routine)):
        curR = routine[i][1]

        if i + 1 < len(routine):
            timeOfAction = routine[i + 1][0] + startTime
            timeForAction = timeOfAction - time.time()

            nxtR = routine[i + 1][1]
            while time.time() < timeOfAction:
                p = 1 - ((timeOfAction - time.time() ) / timeForAction)
                cbFunctions[0](LERPr(curR, nxtR, p), -4)
        else:
            cbFunctions[0](curR, -4)


def waitUntil(timeToWaitFor):
    sleepTime = timeToWaitFor - time.time()
    if sleepTime > 0:
        time.sleep(sleepTime)

def LERPr(cur, nxt, p):
    result = ([0, 0, 0, 0], cur[1])
    for i in range(4):
        result[0][i] = cur[0][i] + (nxt[0][i] - cur[0][i]) * p
    return result
