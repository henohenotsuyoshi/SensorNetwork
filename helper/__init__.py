# -*- coding: utf-8 -*-

'''
さまざまなシーンで利用される関数をもつパッケージ
'''


import math
import numpy as np

__author__ = 'HENOHENOTSUYOSHI'

'''
ノードidの近傍に位置しているアンカーを返す
入力
    ノードのid : id
    アンカーかを表す論理ベクトル : locX
    接続行列 : conX
出力
    隣接するアンカーのインデックス : anchorIndexes
'''
def getNeighborAnhors(n,id,locX,conX):
    anchorIndexes = []
    for i in range(n):
        if locX[i] * conX[id][i] == 1:
            anchorIndexes.append(i)
    return anchorIndexes

def getSortedReliableNodes(_noiseLevel,_anchorIndexes):
    size = len(_anchorIndexes)
    noiseLevel = _noiseLevel[_anchorIndexes].tolist()
    anchorIndexes = []
    for i in range(size):
        d = np.argmin(noiseLevel)
        anchorIndexes.append(_anchorIndexes[d])
        _anchorIndexes.pop(d)
        noiseLevel.pop(d)
    return anchorIndexes

def analyseLocalizability(nSensor,nAnchor,locX):
    nLocSensor = np.sum(locX)-nAnchor
    perLocSensor = nLocSensor/nSensor
    return [nLocSensor,perLocSensor]

def analyseRMSDs(rmsds):
    aveRMSD = sum(rmsds)/len(rmsds)
    minRMSD = min(rmsds)
    maxRMSD = max(rmsds)
    return [aveRMSD,minRMSD,maxRMSD]


def calcRMSD(nSensor,locX,posX,estPosX):
    locSensorX = locX[range(1,nSensor)]
    d = 0
    for i in range(nSensor):
        if locX[i]==1:d+=pow(np.linalg.norm(posX[i]-estPosX[i]),2)
    return math.sqrt(d / np.sum(locSensorX))


def isLocalizable(locX,conX,i):
    if np.dot(locX,conX[i]) >= 3:
        return True
    else:
        return False