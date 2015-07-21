# -*- coding: utf-8 -*-

__author__ = 'HENOHENOTSUYOSHI'

import matplotlib.pyplot as plt
import numpy as np

colors =["#ff0000","#00ff00","#0000ff","#ffff00","#00ffff","#ff00ff"]

def drawClusteredGraph2D(posMat,cHeadVec,clusterVec):
    X = np.array(posMat)[:,0]
    Y = np.array(posMat)[:,1]
    colorsVal = np.random.rand((np.max(cHeadVec)))
    colors = map(lambda clusterNum:colorsVal[clusterNum-1], clusterVec)
    radius = map(lambda cHeadNum:np.pi*(20) if cHeadNum==0 else np.pi*(60),cHeadVec)
    plt.scatter(X,Y,c=colors,s=radius,edgecolor='none')
    plt.show()

def drawHopCountGraph2D(posMat,conMat,hopCountVec):
    nNode = len(conMat)
    X = np.array(posMat)[:,0]
    Y = np.array(posMat)[:,1]
    for i in range(0,nNode):
        plt.text(X[i],Y[i]+0.02,str(hopCountVec[i]),ha='center')
        for j in range(0,nNode):
            if conMat[i][j]:
                plt.plot([posMat[i][0],posMat[j][0]],[posMat[i][1],posMat[j][1]],"c-")
    plt.scatter(X,Y)
    plt.show()