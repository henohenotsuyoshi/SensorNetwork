# -*- coding: utf-8 -*-

'''
作成した問題を保存する
形式は

nSensor,nAnchor,sigma

posX

disX

noisyDisX


'''

import numpy as np

__author__ = 'HENOHENOTSUYOSHI'

def store(fileName,d,nSensor,nAnchor,sigma,posX,disX,noisyDisX):
    f = open(fileName,'w')
    param =""
    param += str(nSensor)+" "
    param += str(nAnchor)+" "
    param += str(sigma)+"\n"

    posXs=""
    disXs=""
    noisyDisXs=""
    for i in range(nSensor+nAnchor):
        st = ""
        for j in range(d):
            st += str(posX[i][j])+" "
        posXs += st +"\n"

    for i in range(nSensor+nAnchor):
        st1 = ""
        st2 = ""
        for j in range(nSensor+nAnchor):
            st1+= str(disX[i][j])+" "
            st2+= str(noisyDisX[i][j])+" "
        disXs += st1 +"\n"
        noisyDisXs += st2 +"\n"

    f.write(param+"\n"+posXs+"\n"+disXs+"\n"+noisyDisXs)
    f.close()

def decord(fileName):
    f = open(fileName)
    data1 = f.read()
    lines =  data1.split('\n')
    print lines

    items1 = lines[0].split(" ")
    nSensor = int(items1[0])
    nAnchor = int(items1[1])
    sigma = float(items1[2])
    n = nSensor + nAnchor

    posX = np.zeros([n,2])
    for i in range(2,2+n):
        item = lines[i]
        items = item.split(" ")
        for j in range(2):
            id = i -2
            posX[id][j] = float(items[j])

    disX = np.zeros([n,n])
    for i in range(3+n,3+2*n):
        item = lines[i]
        items = item.split(" ")
        for j in range(n):
            id = i -3-n
            disX[id][j] = float(items[j])

    noisyDisX = np.zeros([n,n])
    for i in range(4+2*n,4+3*n):
        item = lines[i]
        items = item.split(" ")
        print items
        for j in range(n):
            id = i -4-2*n
            noisyDisX[id][j] = float(items[j])
    f.close()
    return [nSensor,nAnchor,sigma,posX,disX,noisyDisX]
