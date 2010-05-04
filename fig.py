# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np
import matplotlib.pyplot as plt

_subfigs = {}
_timeref = time.time()
numcols = 2

def append(name, y, x=None):
    # ajouter x
    # si x=None -> x = time.time() - _timeref
    _subfigs[name]['data'].append(y)

def subfig(name, title, xlabel, ylabel):
    _subfigs[name] = {'title':title, 'xlabel':xlabel, 'ylabel':ylabel, 'data':[]}

def show():
    n = 0

    for fig in _subfigs.keys():
        numrows = math.ceil(len(_subfigs)/float(numcols))
        n += 1
        plt.subplot(numrows, numcols, n)

        plt.title(_subfigs[fig]['title'])
        plt.xlabel(_subfigs[fig]['xlabel'])
        plt.ylabel(_subfigs[fig]['ylabel'])

        plt.plot(np.array(_subfigs[fig]['data']))

    if n > 0:
        plt.show()
