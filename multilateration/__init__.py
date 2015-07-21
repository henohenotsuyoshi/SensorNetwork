# -*- coding: utf-8 -*-

import numpy as np
import helper

__author__ = 'henohenotsuyoshi'

def getA(baseId,nAnchor,posX):
    A = None
    for i in range(nAnchor):
        if i != baseId:
            ai = np.array([posX[i]-posX[baseId]])
            if A == None:A = ai
            else: A =np.r_[A,ai]
    return A

def getB(baseId,nAnchor,posX,disV):
    b = None
    for i in range(nAnchor):
        if i!= baseId:
            bi = pow(disV[baseId],2)-pow(disV[i],2)-pow(np.linalg.norm(posX[baseId]),2)+pow(np.linalg.norm(posX[i]),2)
            if b == None:b = np.array([bi])
            else: b = np.r_[b,bi]
    return b


def getE1(baseId,nAnchor,disV):
    w = None
    for i in range(nAnchor):
        if i!=baseId:
            wi = 1/(pow(disV[i],2) + pow(disV[baseId],2))
            if w == None:w = np.array([wi])
            else: w = np.r_[w,wi]
    W = np.diag(w)
    return W/np.max(W)

def getE2(radiorange,baseId,nAnchor,disV):
    w = None
    for i in range(nAnchor):
        if i!=baseId:
            wi = radiorange/(radiorange+disV[i])
            if w == None:w = np.array([wi])
            else: w = np.r_[w,wi]
    W = np.diag(w)
    return W/np.max(W)

def getE3(radiorange,sigma,baseId,nAnchor,disV):
    w = None
    for i in range(nAnchor):
        if i!=baseId:
            wi = radiorange/(radiorange+disV[i]*sigma)
            if w == None:w = np.array([wi])
            else: w = np.r_[w,wi]
    W = np.diag(w)
    return W/np.max(W)

'''
getC1とgetCredity1はアンカーの重みをアンカーまでの平均距離数にする
'''
def getC1(radiorange,baseId,nAnchor,creV):
    c = None
    for i in range(nAnchor):
        if i!=baseId:
            ci = 1/(creV[i]+1)
            if c == None:c = np.array([ci])
            else: c = np.r_[c,ci]
    C = np.diag(c)
    return C/np.max(C)

def getCredity1(sigma,radiorange,nAnchor,creV):
    return np.sum(creV)/nAnchor + sigma

def getC2(radiorange,baseId,nAnchor,creV):
    c = None
    for i in range(nAnchor):
        if i!=baseId:
            ci = radiorange/(creV[i]+radiorange)
            if c == None:c = np.array([ci])
            else: c = np.r_[c,ci]
    C = np.diag(c)
    return C/np.max(C)

def getCredity2(sigma,nAnchor,disV,creV):
    return (np.sum(creV)+np.sum(disV)*sigma)/nAnchor

'''
typeW : 観測距離に関する重み
typeC : アンカーの信頼度に関する重み

typeW,typeC=0 : 重みをつけない
typeW=1 : baseIdの分散を考慮する
typeW=2 : baseIdの分散を考慮しない
typeC=1 : アンカーへのホップ数を考慮する
typeC=2 : アンカーへの距離を考慮する
'''
def calcPosition(sigma,radiorange,nAnchor,posX,disV,typeE=0,typeC=0,creV=None):
    if typeC==0:baseId = np.argmin(disV)
    else:
        minC = min(creV)
        candBaseIds = np.where(creV==minC)[0]
        baseId = candBaseIds[ np.argmin(disV[candBaseIds])]
    A = getA(baseId,nAnchor,posX)
    b = getB(baseId,nAnchor,posX,disV)

    if typeE == 0:E = np.identity(nAnchor-1)
    elif typeE == 2: E = getE3(radiorange,sigma,baseId,nAnchor,disV)
    elif typeE == 1: E = getE2(radiorange,baseId,nAnchor,disV)

    if typeC == 0:C = np.identity(nAnchor-1)
    elif typeC == 1: C = getC1(radiorange,baseId,nAnchor,creV)
    elif typeC == 2: C = getC2(radiorange,baseId,nAnchor,creV)

    W = np.dot(C,E)
    ATW = np.dot(A.T,W)
    ATWA = np.dot(ATW,A)
    ATWb = np.dot(ATW,b)
    p = np.dot(np.linalg.inv(ATWA),ATWb)/2
    if typeC == 0:return [p,None]
    elif typeC == 1:return [p,getCredity1(sigma,radiorange,nAnchor,creV)]
    elif typeC == 2:return [p,getCredity2(sigma,nAnchor,disV,creV)]
    return None

def localizeByMultilateration(nSensor,nAnchor,sigma,radiorange,locX,conX,posX,disX,cLevel,typeW,typeC):
    n = nSensor + nAnchor
    nPreLocNode = 0
    nCurLocNode = np.sum(locX)
    while(nPreLocNode<nCurLocNode):
        nPreLocNode = nCurLocNode
        for i in range(nSensor):
            if locX[i] == 0 and helper.isLocalizable(locX,conX,i):
                locX[i] = 1
                anchorIndexes = helper.getNeighborAnhors(n,i,locX,conX)
                nAnchor_neighbor = len(anchorIndexes)
                posX_neighbor = posX[anchorIndexes]
                disX_neighbor = disX[i][anchorIndexes]
                cLevel_neighbor = cLevel[anchorIndexes]
                [p,credity] = calcPosition(sigma,radiorange,nAnchor_neighbor,posX_neighbor,disX_neighbor,typeW,typeC,cLevel_neighbor)
                if credity == None:cLevel[i]=0
                else : cLevel[i] = credity
                posX[i] = p
                # print i
                # print cLevel
        nCurLocNode = np.sum(locX)
    return 0


if __name__=="__main__" :
    nAnchor =4
    posX = np.array([[0.5,0],[0,0.5],[0.5,1],[1,0.5]])
    disV = np.array([0.5,0.5,0.5,1])
    creV = np.array([2.0,1.0,3.0,1.0])

    minC = min(creV)
    candBaseIds = np.where(creV==minC)[0]
    baseId = candBaseIds[ np.argmin(disV[candBaseIds])]
    print baseId

    exit()