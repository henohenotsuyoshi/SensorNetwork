# -*- coding: utf-8 -*-

import pylab
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'HENOHENOTSUYOSHI'

# 2次元平面上に点をプロットする
def plotPoint2D(points,color):
    X =  points[:,0]
    Y = points[:,1]
    plt.plot(points[:,0],points[:,1],"o"+color)

def show():
    plt.show()

def setGraph():
    plt.xlim(xmin=0)
    plt.xlim(xmax=1)
    plt.ylim(ymin=0)
    plt.ylim(ymax=1)

if __name__=="__main__":
    plt.show()