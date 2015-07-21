# -*- coding: utf-8 -*-

import numpy as np

__author__ = 'henohenotsuyoshi'

'''
2次元限定
'''
def inicialLocalize(id,id1,id2,id3,posX,disX):
    x1 = posX[id1][0]
    y1 = posX[id1][1]
    r1 = disX[id][id1]
    x2 = posX[id2][0]
    y2 = posX[id2][1]
    r2 = disX[id][id2]
    x3 = posX[id3][0]
    y3 = posX[id3][1]
    r3 = disX[id][id3]

    A = np.array([[2*(x2-x1),2*(y2-y1)],[2*(x3-x1),2*(y3-y1)]])
    l = np.array([x2*x2 - x1*x1 + y2*y2 - y1*y1 -r2*r2 + r1*r1,x3*x3 - x1*x1 + y3*y3 - y1*y1 -r3*r3 + r1*r1])
    pos = np.dot(l,np.linalg.inv(A).T)
    posX[id] = pos
    return 0

'''
最急降下法でposXを更新する.
ステップサイズはBB法を用いる.
アンカーそれぞれの重みは考慮していない
'''
def descendMethod(id,anchorIndexes,posX,disX):
    return 0