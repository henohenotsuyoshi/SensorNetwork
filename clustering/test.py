# -*- coding: utf-8 -*-

__author__ = 'HENOHENOTSUYOSHI'

import numpy as np
import helper.calc_distance
import clustering.kmeans_approximation as kmeans_approximation
import clustering.graph as graph

def testBasicKMeansApproximation():
    nNode = 500
    k = 20
    posNode = np.random.rand(nNode,2)
    cHeadVec = np.zeros(nNode)
    cHeadVec[0] = 1
    disNode = helper.calc_distance.genDistanceMatrix(posNode)
    (cHeadVec,clusterVec) = kmeans_approximation.kMeansApproximation(disNode,k,cHeadVec)
    graph.drawClusteredGraph2D(posNode,cHeadVec,clusterVec)