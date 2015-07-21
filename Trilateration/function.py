# -*- coding: utf-8 -*-

import math
import numpy as np
import copy

__author__ = 'henohenotsuyoshi'

class DistanceFunction():
    def __init__(self,n,id,posX,disX):
        self.id = id
        self.n = n
        self.posX = posX
        self.disX = disX
        self.iteN = 0
        self.stepSize = 0.01
        self.dx = self.getGradient()

    def getStepSize(self):
        if self.iteN < 100:
            return 0.01
        if self.iteN < 200:
            return 0.005
        if self.iteN < 300:
            return 0.001
        return 0.0005
        # id = self.id
        # if self.iteN <=1:
        #     return 0.01
        # else:
        #     s = self.posX[id] - self.x_
        #     y = self.dx - self.dx_
        #     stepSize = np.dot(s,y) / (pow(np.linalg.norm(y).sum(),2))
        #     if stepSize <0 or stepSize>self.stepSize*100:
        #         stepSize = self.stepSize
        #     return stepSize

    def getValue(self):
        value = 0
        id = self.id
        for i in range(self.n):
            if i != id:
                dif = self.getDif(i)
                value = value + abs(dif)
        return value

    def getDif(self,i):
        id = self.id
        return pow(np.linalg.norm(self.posX[id]-self.posX[i]),2)-pow(self.disX[id][i],2)

    def getGradient(self):
        id = self.id
        gradient = np.array([0.0,0.0])
        for i in range(self.n):
            if i!= id:
                dif = self.getDif(i)
                d = 2*(self.posX[id]-self.posX[i])
                if dif<0:
                    d = -d
                gradient = gradient + d
        return gradient

    def nextStep(self):
        id = self.id
        self.iteN = self.iteN + 1
        self.dx_ = self.dx
        self.dx = self.getGradient()
        self.stepSize = self.getStepSize()
        self.x_ = copy.deepcopy(self.posX[id])
        self.posX[id] = self.posX[id] - self.dx * self.stepSize

'''
インデックス 1~nSensor のセンサーの位置を再急降下法により更新する
'''
class DistanceFunction1():
    def __init__(self,nSensor,nAnchor,posX,disX,conX):
        self.nSensor = nSensor
        self.nAnchor = nAnchor
        self.posX = posX
        self.disX = disX
        self.conX = conX
        self.iteN = 0
        self.stepSize = 0.001
        self.dx = self.getGradient()

    def getStepSize(self):
        return 0.001

    def getValue(self):
        value = 0
        # センサー間の目的関数値計算
        for i in range(self.nSensor):
            for j in range(i,self.nSensor+self.nAnchor):
                if self.conX[i][j] ==1 :
                    value += abs(self.getDif(i,j))
        return value

    def getDif(self,i,j):
        return pow(np.linalg.norm(self.posX[i]-self.posX[j]),2)-pow(self.disX[i][j],2)

    # この関数の微分を求める形式は 2*nSensorの行列
    def getGradient(self):
        gradient = []
        for i in range(self.nSensor):
            gradient.append(self.getIDGradient(i))
        return np.array(gradient)

    # センサーidの微分を求める
    def getIDGradient(self,id):
        gradient = np.array([0.0,0.0])
        for i in range(self.nSensor + self.nAnchor):
            if self.conX[id][i] == 1:
                dif = self.getDif(id,i)
                d = 2*(self.posX[id]-self.posX[i])
                if dif<0:
                    d = -d
                gradient += d
                print gradient
        print "finaly"
        print gradient
        return gradient

    def nextStep(self):
        self.iteN +=1
        self.dx_ = self.dx
        self.dx = self.getGradient()
        self.stepSize = self.getStepSize()
        self.posX_ = copy.deepcopy(self.posX)
        idSensors = range(self.nSensor)
        print self.dx
        print self.stepSize
        self.posX[idSensors] = self.posX[idSensors] - self.dx * self.stepSize