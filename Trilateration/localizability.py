# -*- coding: utf-8 -*-

import numpy as np

__author__ = 'henohenotsuyoshi'


def isLocalizable(locX,conX,i):
    if np.dot(locX,conX[i]) >= 3:
        return True
    else:
        return False
