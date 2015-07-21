__author__ = 'HENOHENOTSUYOSHI'

import numpy as np
import copy

WHITE = -1
BLACK = 1

class Node:
    def __init__(self,index,num,depth):
        self.index = index
        self.num = num
        self.next = None
        self.child = None
        self.depth = depth
        self.lowpt = None
        self.nChild = 0
        self.isJoint = False

    def addChild(self,child):
        if(self.child == None):
            self.child = child
        else:
            self.child.next = child
        self.nChild += 1

    def toString(self):
        if self.lowpt == None:
           return u"index: %d, num: %d, depth: %d, nChild: %d, isJoint: %r"%(self.index,self.num,self.depth,self.nChild,self.isJoint)
        else:
            return u"index: %d, num: %d, depth: %d, nChild: %d, isJoint: %r, lowpt: %d"%(self.index,self.num,self.depth,self.nChild, self.isJoint,self.lowpt)

def setLowpt(markedNodes,markedEdges,conMat,nNode,node):
    if node == None:
        return
    lowpt = node.num
    child = node.child
    while child != None:
        setLowpt(markedNodes,markedEdges,conMat,nNode,child)
        lowpt = min(lowpt,child.lowpt)
        child = child.next
    for i in range(0,nNode):
        if conMat[i][node.index] and markedEdges[i][node.index] == WHITE:
            lowpt = min(lowpt,markedNodes[i])
    node.lowpt = lowpt

def setIsJoint(conMat,nNode,node):
    if node == None:
        return
    setIsJoint(conMat,nNode,node.child)
    setIsJoint(conMat,nNode,node.next)
    child = node.child
    while(child != None):
        if(node.num <= child.lowpt):
            markedNodes = np.zeros(nNode) -1
            markedEdges = np.zeros([nNode,nNode]) -1
            num = [0]
            root = depthFirstSearch(node.index,num,0,markedNodes,markedEdges,conMat,nNode)
            if root.nChild >= 2:
                node.isJoint = True
            break
        child = child.next


def depthFirstSearch(index,num,depth,markedNodes,markedEdges,conMat,nNode):
    node = Node(index,num[0],depth)
    markedNodes[index] = num[0]
    for i in range(0,nNode):
        if markedNodes[i] == WHITE and conMat[i][index] == 1:
            markedEdges[i][index] = BLACK
            markedEdges[index][i] = BLACK
            num[0] = num[0] + 1
            node.addChild(depthFirstSearch(i,num,depth+1,markedNodes,markedEdges,conMat,nNode))
    return node

def findJointNodesIndex_Helper(node,indexes):
    if node == None:
        return
    if node.isJoint:
        indexes.append(node.index)
    findJointNodesIndex_Helper(node.child,indexes)
    findJointNodesIndex_Helper(node.next,indexes)

def findJointNodesIndex(root):
    indexes = []
    findJointNodesIndex_Helper(root,indexes)
    return indexes

def findConnectedComponents(conMat):
    nNode = len(conMat)
    markedNodes = np.zeros(nNode) -1
    markedEdges = np.zeros([nNode,nNode]) -1
    num = [0]
    node = depthFirstSearch(0,num,0,markedNodes,markedEdges,conMat,nNode)
    setLowpt(markedNodes,markedEdges,conMat,nNode,node)
    setIsJoint(conMat,nNode,node)
    jointIndexes = findJointNodesIndex(node)
    isJointNodes = np.zeros(nNode)
    for k in jointIndexes:
        isJointNodes[k] = 1
    conMat_disjoint = copy.deepcopy(conMat)
    for i in jointIndexes:
        for j in range(0,nNode):
            conMat_disjoint[i][j] = 0
            conMat_disjoint[j][i] = 0
    markedNodes = np.zeros(nNode) - 1
    isConnectedComps = []
    for i in range(0,nNode):
        if not isJointNodes[i] and markedNodes[i] == -1:
            markedNodes_d = np.zeros(nNode)-1
            markedEdges_d = np.zeros([nNode,nNode])-1
            isConnectedComp = np.zeros(nNode)
            num_comp = [0]
            depthFirstSearch(i,num_comp,0,markedNodes_d,markedEdges_d,conMat_disjoint,nNode)
            for k in range(0,nNode):
                if markedNodes_d[k] >= 0:
                    isConnectedComp[k] = 1

            for k in jointIndexes:
                for j in range(0,nNode):
                    if conMat[k][j] == 1 and markedNodes_d[j] >=0:
                        isConnectedComp[k] = 1

            for k in range(0,nNode):
                if markedNodes_d[k] >= 0:
                    markedNodes[k] = 1
            isConnectedComps.append(isConnectedComp)
    return isConnectedComps

def printTree(node):
    if node == None:
        return
    space = ""
    for i in range(0,node.depth):
        space = space + " "
    print space + node.toString()
    printTree(node.child)
    printTree(node.next)

def isTwoConnected(conMat):
    for conVec in conMat:
        if np.sum(conVec) < 2:
            return False
    return True

if __name__ == "__main__":
    conMat = np.zeros([8,8])
    conMat[0][1] = 1
    conMat[0][2] = 1
    conMat[0][3] = 1
    conMat[1][0] = 1
    conMat[1][2] = 1
    conMat[1][4] = 1
    conMat[1][6] = 1
    conMat[1][7] = 1
    conMat[2][0] = 1
    conMat[2][1] = 1
    conMat[2][3] = 1
    conMat[3][0] = 1
    conMat[3][2] = 1
    conMat[4][1] = 1
    conMat[4][5] = 1
    conMat[4][6] = 1
    conMat[5][4] = 1
    conMat[5][6] = 1
    conMat[6][1] = 1
    conMat[6][4] = 1
    conMat[6][5] = 1
    conMat[6][7] = 1
    conMat[7][1] = 1
    conMat[7][6] = 1
    isConnectedComps = findConnectedComponents(conMat)
    print isConnectedComps
    print len(isConnectedComps)
    print len(isConnectedComps[0])