# -*- coding: utf-8 -*-

'''
実際に計算を行うパッケージ
'''

import problems
import sys
import Trilateration as tri
import Multilateration as multi
import helper
import graph

__author__ = 'HENOHENOTSUYOSHI'


# グラフの疎密性からパラメータを決定するためのプログラム
def paramSearch(d,nSensor,nAnchor,radiorange,iteN):
    sumLocSensor = 0
    minNLocSensor = sys.maxint
    maxNLocSensor = 0
    for i in range(iteN):
        [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange,i)
        tri.checkLocalizability(nSensor,locX,conX)
        [nLocSensor,preLocSensor] = helper.analyseLocalizability(nSensor,nAnchor,locX)
        sumLocSensor += nLocSensor
        minNLocSensor = min(minNLocSensor,nLocSensor)
        maxNLocSensor = max(maxNLocSensor,nLocSensor)
        print nLocSensor
    aveNLocSensor = sumLocSensor / iteN
    perLocSensor = aveNLocSensor/nSensor
    perMinLocSensor = minNLocSensor / nSensor
    perMaxLocSensor = maxNLocSensor / nSensor
    return [perLocSensor,perMinLocSensor,perMaxLocSensor]


# ノイズの増加による精度の低下を表す図を作成するためのプログラム
# 位置推定にはシンプルなMultilaterationを用いる
def noiseImpactSearch(d,nSensor,nAnchor,sigmas,radiorange):
    graph.setLimit()
    for i in range(len(sigmas)):
        graph.setGraph()

        [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange,0)
        multi.localizeByMultilateration(nSensor,nAnchor,locX,conX,estPosX,noisyDisX,cLevel,0,0)
        rmsd = helper.calcRMSD(nSensor,locX,posX,estPosX)
        graph.plotPoint2D(estPosX,"")
        print rmsd
    graph.show()



# Trilaterationを走らせるためのプログラム
def calcPosition_Trilateration(d,nSensor,nAnchor,sigma,radiorange,iteN,type):
    print "Trilaterationによる位置計算を開始"
    locSensorNs = []
    RMSDs =[]
    for i in range(iteN):
        [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange,i+100)
        if type==1:tri.localizeByTrilateration(nSensor,nAnchor,locX,conX,estPosX,noisyDisX,cLevel)
        [nLocSensor,preLocSensor] = helper.analyseLocalizability(nSensor,nAnchor,locX)

        locSensorNs.append(nLocSensor)
        rmsd = helper.calcRMSD(nSensor,locX,posX,estPosX)
        RMSDs.append(rmsd)

        print nLocSensor
        print rmsd
    perLocSensor = sum(locSensorNs)/nSensor/iteN
    perMinLocSensor = min(locSensorNs)/nSensor
    perMaxLocSensor = max(locSensorNs)/nSensor
    [aveRMSD,minRMSD,maxRMSD] = helper.analyseRMSDs(RMSDs)
    RMSDsModified = [elem for elem in RMSDs if elem<1]
    [aveRMSD_modified,a,b]= helper.analyseRMSDs(RMSDsModified)
    return [perLocSensor,perMinLocSensor,perMaxLocSensor,aveRMSD,minRMSD,maxRMSD,aveRMSD_modified]


# Multilaterationを走らせるためのプログラム
def calcPosition_Multilateration(d,nSensor,nAnchor,sigma,radiorange,iteN,typeE,typeC):
    print "Multilateraitonによる位置計算を開始"
    print ""
    locSensorNs = []
    RMSDs =[]
    RMSDs_modified=[]
    i=0
    breachN = 0
    while i-breachN < iteN:
        [posX,locX,disX,conX,noisyDisX,trueDisX,estPosX,cLevel] = problems.createProblem_random(d,nSensor,nAnchor,sigma,radiorange,i)
        multi.localizeByMultilateration(nSensor,nAnchor,sigma,radiorange,locX,conX,estPosX,noisyDisX,cLevel,typeE,typeC)
        [nLocSensor,preLocSensor] = helper.analyseLocalizability(nSensor,nAnchor,locX)
        locSensorNs.append(nLocSensor)
        rmsd = helper.calcRMSD(nSensor,locX,posX,estPosX)
        RMSDs.append(rmsd)
        if rmsd <1.5:
            RMSDs_modified.append(rmsd)
        else: breachN +=1
        i+=1
        print rmsd
    perLocSensor = sum(locSensorNs)/nSensor/iteN
    perMinLocSensor = min(locSensorNs)/nSensor
    perMaxLocSensor = max(locSensorNs)/nSensor
    [aveRMSD,minRMSD,maxRMSD] = helper.analyseRMSDs(RMSDs)

    [aveRMSD_modified,minRMSD_modified,maxRMSD_modified]= helper.analyseRMSDs(RMSDs_modified)
    return [perLocSensor,perMinLocSensor,perMaxLocSensor,aveRMSD,minRMSD,maxRMSD,aveRMSD_modified,breachN]


if __name__ == "__main__":
    d = 2
    nSensor=100
    nAnchor=60
    sigma = 0.08
    radiorange=0.13
    iteN = 100


    # [perLocSensor,perMinLocSensor,perMaxLocSensor] = paramSearch(d,nSensor,nAnchor,radiorange,iteN)


    # sigmas = [0.01,0.05,0.09]
    # noiseImpactSearch(d,nSensor,nAnchor,sigmas,radiorange)

    # type = 1
    # [perLocSensor,perMinLocSensor,perMaxLocSensor,aveRMSD,minRMSD,maxRMSD,aveRMSD_modified] = calcPosition_Trilateration(d,nSensor,nAnchor,sigma,radiorange,iteN,type)


    typeE=2
    typeC=2
    [perLocSensor,perMinLocSensor,perMaxLocSensor,aveRMSD,minRMSD,maxRMSD,aveRMSD_modified,breachN] = calcPosition_Multilateration(d,nSensor,nAnchor,sigma,radiorange,iteN,typeE,typeC)