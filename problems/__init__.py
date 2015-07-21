# -*- coding: utf-8 -*-

'''
センサーネットワークの問題を作成するためのパッケージ
'''

import create
import store
import graph


__author__ = 'henohenotsuyoshi'

def createProblem_random(d,nSensor,nAnchor,sigma=0,radiorange=1000,seed = None):
    n = nSensor + nAnchor
    posX = create.createPositions_random(d,n,seed)
    locX = create.createLocMatrix(nSensor,nAnchor)
    disX = create.createDistanceMatrix(nSensor,nAnchor,n,posX,radiorange)
    conX = create.createConnectedMatrix(n,disX, radiorange)
    noisyDisX = create.addNoise(n,disX,sigma)
    trueDisX = create.createDistanceMatrix(nSensor,nAnchor,n,posX,3000)
    estPosX = create.createEstPositionMatrix(d,nSensor,posX)

    noiseLevel = create.createNoiseLevel(nSensor,nAnchor,n)
    cLevel = create.createCredityLevel(nSensor,nAnchor)

    return [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel]

def storeProblem(filename,d,nSensor,nAnchor,sigma,posX,trueDisX,noisyDisX):
    store.store(filename,d,nSensor,nAnchor,sigma,posX,trueDisX,noisyDisX)

def restoreProblem(filename,radiorange):
    [nSensor,nAnchor,sigma,posX,trueDisX,noisyDisX] = store.decord(filename)
    estPosX = create.createEstPositionMatrix(2,nSensor,posX)
    locX = create.createLocMatrix(nSensor,nAnchor)


def drawNetwork1(nSensor,nAnchor,locX,posX,estPosX):
    graph.drawGraph1(nSensor,nAnchor,locX,posX,estPosX)

def drawNetwork2(nSensor,nAnchor,locX,posX,estPosX,estPosX2):
    graph.drawGraph2("problem100_100.txt",nSensor,nAnchor,locX,posX,estPosX,estPosX2)




if __name__ =="__main__":

    d=2
    nSensor=3
    nAnchor=3
    sigma=0.1*0.1
    radiorange= 0.4
    [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,noiseLevel] = createProblem_random(d,nSensor,nAnchor,sigma,radiorange)
    storeProblem("problem100_100.txt",d,nSensor,nAnchor,sigma,posX,trueDisX,noisyDisX)
    print disX
    print trueDisX
    # store.decord("problem100_100.txt")