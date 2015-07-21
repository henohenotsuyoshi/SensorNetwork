__author__ = 'HENOHENOTSUYOSHI'

import sys
import math

'''
all disMat[i][j] should be below radiorange
'''
def twohop_distance(nNode, disMat, conMat):
    dMat = [[sys.maxint for i in xrange(nNode)] for j in xrange(nNode)]
    for i in xrange(nNode):
        for j in xrange(nNode):
            if conMat[i][j] == 1:
                for k in xrange(nNode):
                    if conMat[j][k] == 1:
                        dMat[i][k] = min(dMat[i][k], disMat[i][j] + disMat[j][k])
                        dMat[k][i] = dMat[i][k]

    for i in xrange(nNode):
        dMat[i][i] = 0
        for j in xrange(nNode):
            if conMat[i][j] == 1 or dMat[i][j] == sys.maxint:
                dMat[i][j] = 0
                dMat[j][i] = 0

    cMat = [[1 if dMat[i][j] > 0 else 0 for i in xrange(nNode)] for j in xrange(nNode)]
    return [dMat, cMat]

'''
compare two distance matrixes and print some results
'''
def compare_distances(nSensor, nNode, disMat1, disMat2, conMat):
    ave = 0.
    count = 0
    perPositive = 0.
    for i in xrange(nSensor):
        for j in xrange(i, nNode):
            if conMat[i][j] == 1:
                count += 1
                dif = disMat1[i][j] - disMat2[i][j]
                ave += dif
                if dif > 0: perPositive += 1
    ave /= count
    perPositive /= count
    print "count : %d" % count
    print "ave : %f" % ave
    print "percent of positive : %f" % perPositive

def get_ave_degree(nSensor, nNode, conMat):
    ave = 0.
    for i in xrange(nSensor):
        for j in xrange(nNode):
            ave += conMat[i][j]
    return ave / nSensor

if __name__=="__main__":
    import problems
    d = 2
    nSensor = 100
    nAnchor = 100
    nNode = nSensor + nAnchor
    sigma = 0.1
    radiorange = 0.1
    [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,noiseLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange)

    print get_ave_degree(nSensor, nNode, conX)
    [dMat, cMat] = twohop_distance(nSensor + nAnchor, noisyDisX, conX)

    compare_distances(nSensor, nSensor + nAnchor, disX, noisyDisX, conX)
    compare_distances(nSensor, nSensor + nAnchor, dMat, trueDisX, cMat)



    '''
    nSensor = 6
    nNode = 6
    disMat = [[0., 0.707, 0.4, 0.583, 0.,0.],[0.707, 0., 0.51, 0., 0.707,0.],[0.4, 0.51, 0. ,0.6, 0.316,0.],[0.583, 0, 0.6, 0, 0.583,0.],[0, 0.707, 0.316, 0.583,0.,0.5],[0, 0., 0., 0.,0.5,0.]]
    conMat = [[0 if disMat[j][i] == 0 else 1 for i in xrange(nNode)] for j in xrange(nNode)]
    print disMat
    print conMat
    twohop_distance(nSensor, nNode, disMat, conMat)
    '''