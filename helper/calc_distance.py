# -*- coding: utf-8 -*-

import numpy as np

__author__ = 'HENOHENOTSUYOSHI'

'''
入力:
    ノードの位置行列 : posNode
出力:
    ノードの距離行列 : disNode
'''
def genDistanceMatrix(_posNode):
    nNode = len(_posNode)
    posNode = np.array(_posNode)
    disNode = np.zeros([nNode,nNode])
    for i in range(0,nNode):
        for j in range(0,nNode):
            disNode[i][j] = np.linalg.norm(posNode[i]-posNode[j])
    return disNode

'''
    disX=np.zeros([n,n])
    for i in range(nSensor):
        for j in range(nSensor):
            distance = np.linalg.norm(posX[i]-posX[j])
            if(distance <radiorange):
               disX[i][j] = distance
        for j in range(nSensor,nSensor+nAnchor):
            distance = np.linalg.norm(posX[i]-posX[j])
            if(distance <radiorange):
                disX[i][j] = distance
                disX[j][i] = distance
    for i in range(nSensor,nSensor + nAnchor):
        for j in range(nSensor,nSensor + nAnchor):
            distance = np.linalg.norm(posX[i]-posX[j])
            disX[i][j] = distance
    return np.array(disX)
'''