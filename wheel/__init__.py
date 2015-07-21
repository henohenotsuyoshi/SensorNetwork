from IPython.nbconvert.filters.markdown import marked

__author__ = 'HENOHENOTSUYOSHI'

import numpy as np
import graph.component as component
import copy

def isWheelHub(hub,conMat):
    n = len(conMat)
    cycleConMat = copy.deepcopy(conMat)
    cycleConMat = np.delete(cycleConMat,hub,0)
    cycleConMat = np.delete(cycleConMat,hub,1)
    for comp in component.findConnectedComponents(cycleConMat):
        indexes = np.where(comp==0)[0]
        indexes =  indexes[::-1]
        compConMat = copy.deepcopy(cycleConMat)
        for j in indexes:
            compConMat = np.delete(compConMat,j,0)
            compConMat = np.delete(compConMat,j,1)

        if component.isTwoConnected(compConMat):
            return True
    return False

if __name__ == "__main__":
    conMat = np.zeros([6,6])
    conMat[0][1] = 1
    conMat[0][2] = 1
    conMat[0][3] = 1
    conMat[0][4] = 1
    conMat[0][5] = 1
    conMat[1][0] = 1
    conMat[1][2] = 1
    conMat[1][3] = 1
    conMat[1][4] = 1
    conMat[2][0] = 1
    conMat[2][1] = 1
    conMat[2][3] = 1
    conMat[3][0] = 1
    conMat[3][1] = 1
    conMat[3][2] = 1
    conMat[4][0] = 1
    conMat[4][1] = 1
    conMat[4][5] = 1
    conMat[5][0] = 1
    conMat[5][4] = 1
    print conMat
    print isWheelHub(0,conMat)