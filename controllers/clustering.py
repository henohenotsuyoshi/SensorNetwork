__author__ = 'HENOHENOTSUYOSHI'

import problems
import wheel
import numpy as np
import pylab

def clusteringByWheel(d,nSensor,radiorange):
    [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel] = problems.createProblem_random(d,nSensor,0,0,radiorange)
    nNode = len(conX)
    isWheelHub = np.zeros(nNode)
    for i in range(0,nNode):
        c = conX[i]
        indexes = np.where(c == 1)[0]
        if len(indexes) >=3:
            indexes = np.insert(indexes,0,i)
            localConX = np.array([[conX[k][j] for k in indexes] for j in indexes])
            if wheel.isWheelHub(0,localConX):
                isWheelHub[i] = 1

    for i in range(nNode):
        if isWheelHub[i] == 1:
            dot = "or"
        else :
            dot = "ob"
        pylab.plot(posX[i][0],posX[i][1],dot)
        for j in range(nNode):
            if conX[i][j] == 1:
                pylab.plot([posX[i][0],posX[j][0]],[posX[i][1],posX[j][1]],"g-")
    pylab.show()




if __name__ == "__main__":
    clusteringByWheel(2,1000,0.055)