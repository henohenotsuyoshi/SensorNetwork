# -*- coding: utf-8 -*-

'''
センサーネットワークの問題を作成するモジュール
'''

import random as rand
import numpy as np
import sys
import copy

__author__ = 'henohenotsuyoshi'

'''
点がランダムに配置されたネットワークを作成する
入力
    次元:d
    センサーの数:n
出力
    位置を表す行列(np.array):X in R^(d*n)
'''
def createPositions_random(d,n,seed):
    posX = []
    if seed != None:rand.seed(seed)
    for i in range(n):
        position = []
        for j in range(d):
            position.append(rand.random())
        posX.append(position)
    return np.array(posX)

'''
距離行列を返す
入力
    センサーの数 : n
    位置行列 : X
    通信可能な限界距離 : radiorange
出力
    距離行列 : disX in R^(n*n)
'''

def createDistanceMatrix(nSensor,nAnchor,n,posX,radiorange):
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
接続行列を返す
入力
    センサーの数 : n
    距離行列 : disX
出力
    接続行列 : conX
'''
def createConnectedMatrix(n, disX, radiorange):
    conX = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            if(disX[i][j]!=0 and disX[i][j] < radiorange):
                conX[i][j] = 1
    return conX

'''
距離行列にノイズを加える
ノイズは真の距離に平均0,分散sigmaの正規分布を掛けた値を入力されたdisXに加えたもの
入力
    センサーの数 : n
    距離行列 : disX
    分散 : sigma
出力
    距離行列 : disX in R^(n*n)
'''
def addNoise(n,disX,sigma):
    noisyDisX = np.zeros([n,n])
    for i in range(n):
        for j in range(i,n):
            distance = disX[i][j]
            if distance !=0:
                noisyDis = distance + rand.gauss(0,sigma)*distance
                noisyDisX[i][j] = noisyDis
                noisyDisX[j][i] = noisyDis
    return noisyDisX

'''
論理ベクトルの初期解を作成
'''
def createLocMatrix(nSensor,nAnchor):
    z = np.zeros(nSensor)
    o = np.ones(nAnchor)
    return np.append(z,o)

'''
ノイズレベルベクトルを作成
'''
def createNoiseLevel(nSensor,nAnchor,n):
    s = np.zeros(nSensor)
    for i in range(nSensor):
        s[i] = sys.maxint
    a = np.zeros(nAnchor)
    return np.append(s,a)

'''
信頼度を作成
'''
def createCredityLevel(nSensor,nAnchor):
    c = np.zeros(nSensor+nAnchor)
    for i in range(nSensor):
        c[i] = sys.maxint
    return c

'''
位置推定のための行列を作成
'''
def createEstPositionMatrix(d,nSensor,posX):
    estPosX = copy.deepcopy(posX)
    for i in range(nSensor):
        for j in range(d):
            estPosX[i][j] = 0
    return estPosX

'''
真の距離行列から距離行列,接続行列,ノイズを含む行列を作成
'''
def createParams(n,trueDisX,noisyDisX_,radiorange):
    conX = np.zeros([n,n])
    disX = np.zeros([n,n])
    noisyDisX = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            if trueDisX[i][j] < radiorange:
                conX[i][j] = 1
                disX[i][j] = trueDisX[i][j]
                noisyDisX[i][j] = noisyDisX_[i][j]
    return [conX,disX,noisyDisX]