# -*- coding: utf-8 -*-

__author__ = 'HENOHENOTSUYOSHI'

import numpy as np
import helper.calc_distance
import graph
import sys

'''
root nodeからの最小のHOP回数を求める
入力:
    root nodeのインデックス : root
    接続行列 : conMat
出力:
    HOP回数を表すベクトル : hopVec(到達不可能な場合は∞)
'''

def getHopCount(conMat,root):
    nNode = len(conMat)
    hopCountVec = np.zeros(nNode) + sys.maxint
    hopCountVec[root] = 0
    return hopCountVec

def isConnectedToUncheckedNode(conMat,root,isCheckedVector):

    return

if __name__ == "__main__":
    nNode = 20
    posMat = np.random.rand(nNode,2)
    radiorange = 0.3
    disMat = helper.calc_distance.genDistanceMatrix(posMat)
    f = lambda distance:1 if distance<radiorange and distance != 0 else 0
    conMat = [[f(disMat[i][j]) for j in range(0,nNode)] for i in range(0,nNode)]
    hopCountVec = np.zeros(nNode)
    print getHopCount(conMat,1)
    graph.drawHopCountGraph2D(posMat,conMat,hopCountVec)