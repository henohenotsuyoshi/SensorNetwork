# -*- coding: utf-8 -*-

'''
Trilaterationのためのパッケージ
'''
import problems
import numpy as np
import copy
import time
import localizability
import localize
import function
import helper
import pylab

__author__ = 'henohenotsuyoshi'


def checkLocalizability(nSensor,locX,conX):
    nPreLocNode = 0
    nCurLocNode = np.sum(locX)
    while(nPreLocNode<nCurLocNode):
        nPreLocNode = nCurLocNode
        for i in range(nSensor):
            if localizability.isLocalizable(locX,conX,i):
                locX[i] = 1
        nCurLocNode = np.sum(locX)


"""
Trilaterationにより位置決定可能な全てのセンサーの位置を決定する.
なお,Trilaterationによる位置推定では信頼度が最も小さい3つを選ぶ
"""
def localizeByTrilateration(nSensor,nAnchor,locX,conX,posX,disX,noiseLevel):
    n = nSensor + nAnchor
    nPreLocNode = 0
    nCurLocNode = np.sum(locX)
    while(nPreLocNode<nCurLocNode):
        nPreLocNode = nCurLocNode
        for i in range(nSensor):
            if (localizability.isLocalizable(locX,conX,i) and locX[i]==0):
                locX[i] = 1
                anchorIndexes = helper.getNeighborAnhors(n,i,locX,conX)
                anchorIndexes = helper.getSortedReliableNodes(noiseLevel,anchorIndexes)
                localize.inicialLocalize(i,anchorIndexes[0],anchorIndexes[1],anchorIndexes[2],posX,disX)
                noiseLevel[i] = 3
        nCurLocNode = np.sum(locX)


'''
Trilaterationにより位置決定可能な全てのセンサーの位置を決定する
なお,Trilaterationによる推定位置を初期位置として再急降下を実行する
'''
def localizeByTrilateration_1(nSensor,nAnchor,locX,conX,posX,disX,noiseLevel):
    n = nSensor + nAnchor
    nPreLocNode = 0
    nCurLocNode = np.sum(locX)
    while nPreLocNode < nCurLocNode:
        nPreLocNode = nCurLocNode
        for i in range(nSensor):
            if localizability.isLocalizable(locX,conX,i) and locX[i] == 0:
                locX[i] = 1
                anchorIndexes = helper.getNeighborAnhors(n,i,locX,conX)
                anchorIndexes = helper.getSortedReliableNodes(noiseLevel,anchorIndexes)
                localize.inicialLocalize(i,anchorIndexes[0],anchorIndexes[1],anchorIndexes[2],posX,disX)
                noiseLevel[i] = 3
        nCurLocNode = np.sum(locX)
    return 0

def test():
    posX = np.array([[0,0],[0.5,0],[0,0.5],[0.5,1]])
    disX = np.array([[0,0.5,0.5,0.5,0.5],
                     [0.5,0,0.7,1],
                     [0.5,0.7,0,0.7],
                     [0.5,1,0.7,0]])
    conX = np.array([[0,1,1,1],
                     [1,0,1,1],
                     [1,1,0,1],
                     [1,1,1,0]])
    return [posX,disX,conX]

def drawGraph1(nSensor,nAnchor,locX,posX,estPosX):
    # センサーをプロット
    for i in range(nSensor):
        if locX[i]==1:
            pylab.plot([posX[i][0],estPosX[i][0]],[posX[i][1],estPosX[i][1]],"g-")
            pylab.plot(posX[i][0],posX[i][1],"ob")
            pylab.plot(estPosX[i][0],estPosX[i][1],"oc")
        else :
            pylab.plot(posX[i][0],posX[i][1],"xb")
    # アンカーをプロット
    for i in range(nSensor,nSensor+nAnchor):
        pylab.plot(posX[i][0],posX[i][1],"or")

def drawGraph2(nSensor,nAnchor,locX,posX,estPosX,estPosX2):
    # センサーをプロット
    for i in range(nSensor):
        if locX[i]==1:
            pylab.plot(posX[i][0],posX[i][1],"ob")
            pylab.plot(estPosX[i][0],estPosX[i][1],"oc")
            pylab.plot(estPosX2[i][0],estPosX2[i][1],"og")
        else :
            pylab.plot(posX[i][0],posX[i][1],"xb")
    # アンカーをプロット
    for i in range(nSensor,nSensor+nAnchor):
        pylab.plot(posX[i][0],posX[i][1],"or")

if __name__ == "__main__":
    d=2
    nSensor=5
    nAnchor=5
    sigma=0.1
    radiorange=20
    [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,noiseLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange)
    localizeByTrilateration(nSensor,nAnchor,locX,conX,estPosX,noisyDisX,noiseLevel)
    estPosX2 = copy.deepcopy(estPosX)
    # func = function.DistanceFunction(0,3,estPosX,noisyDisX)
    func = function.DistanceFunction1(nSensor,nAnchor,posX,noisyDisX,conX)
    print func.getValue()
    # print func.posX
    for i in range(10):
        if np.linalg.norm(func.dx)<0.001:break
        func.nextStep()
    print posX[0]
    print estPosX2
    print estPosX
    drawGraph1(nSensor,nAnchor,locX,posX,estPosX)
    pylab.show()
    # print func.posX
    exit()