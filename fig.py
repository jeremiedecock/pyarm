# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np
import matplotlib.pyplot as plt
import warnings
import numbers

_subfigs  = {}
_timeref  = time.time()
_filename = "fig.png"
_save     = True

def append(name, y, x=None):
    if name in _subfigs:

        if x is None:
            x = time.time() - _timeref

        if isinstance(x, numbers.Number):
            _subfigs[name]['xdata'].append(x)
        elif isinstance(x, np.ndarray):
            _subfigs[name]['xdata'].append(x.copy())
        else:
            raise TypeError('x type is ' + str(type(x)) + ' (number or array expected)')

        if isinstance(y, numbers.Number):
            _subfigs[name]['ydata'].append(y)
        elif isinstance(y, np.ndarray):
            _subfigs[name]['ydata'].append(y.copy())
        else:
            raise TypeError('y type is ' + str(type(y)) + ' (number or array expected)')

    else:
        warnings.warn('"' + str(name) + '" has not been declared with fig.subfig(). "' + str(name) + '" is not defined in _subfigs.')

def subfig(name, title=None, xlabel='', ylabel='', type='plot', axis=None):
    if title is None: title = str(name)
    _subfigs[name] = {'title':title, 'xlabel':xlabel, 'ylabel':ylabel, 'type':type, 'axis':axis, 'xdata':[], 'ydata':[]}

def show(numcols=2):
    n = 0

    for fig in _subfigs:
        n += 1
        numrows = math.ceil(len(_subfigs)/float(numcols))
        plt.subplot(numrows, numcols, n)

        # Set labels
        plt.title(_subfigs[fig]['title'])
        plt.xlabel(_subfigs[fig]['xlabel'])
        plt.ylabel(_subfigs[fig]['ylabel'])

        # Fetch datas
        x = np.array(_subfigs[fig]['xdata'])
        y = np.array(_subfigs[fig]['ydata'])

        # Plot
        if _subfigs[fig]['type'] == 'fill':
            plt.fill(x, y, alpha=0.2)
        else:
            plt.plot(x, y)

        # Set axis limits
        if isinstance(_subfigs[fig]['axis'], list):
            if len(_subfigs[fig]['axis']) >= 2:
                plt.xlim(_subfigs[fig]['axis'][0], _subfigs[fig]['axis'][1])
            if len(_subfigs[fig]['axis']) >= 4:
                plt.ylim(_subfigs[fig]['axis'][2], _subfigs[fig]['axis'][3])

    if n > 0:
        if _save: plt.savefig(_filename, dpi=300)
        plt.show()

