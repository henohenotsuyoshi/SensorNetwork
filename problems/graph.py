# -*- coding: utf-8 -*-

'''
グラフを出力する
'''

import pylab

__author__ = 'HENOHENOTSUYOSHI'

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