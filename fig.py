# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np
import matplotlib.pyplot as plt
import warnings

_subfigs   = {}
_timeref   = time.time()
_filename  = "fig.png"
_save      = False
delta_time = 0.

def append(name, y, x=None):
    if name in _subfigs:

        if x is None:
            if delta_time > 0:
                x = len(_subfigs[name]['xdata']) * delta_time
            else:
                # realtime simulation
                x = time.time() - _timeref

        #if isinstance(x, numbers.Number):
        if not hasattr(x, 'copy'):
            _subfigs[name]['xdata'].append(x)
        #elif isinstance(x, np.ndarray):
        else:
            _subfigs[name]['xdata'].append(x.copy())

        #if isinstance(y, numbers.Number):
        if not hasattr(y, 'copy'):
            _subfigs[name]['ydata'].append(y)
        #elif isinstance(y, np.ndarray):
        else:
            _subfigs[name]['ydata'].append(y.copy())

    else:
        warnings.warn('"' + str(name) +
                      '" has not been declared with fig.subfig(). "'
                      + str(name) + '" is not defined in _subfigs.')

def subfig(name, title=None, xlabel='', ylabel='', type='plot', xlim=None,
           ylim=None, legend=None):
    if title is None:
        title = str(name)
    _subfigs[name] = {'title':title, 'xlabel':xlabel, 'ylabel':ylabel,
                      'type':type, 'xlim':xlim, 'ylim':ylim, 'legend':legend,
                      'xdata':[], 'ydata':[]}

def show(numcols=2):
    n = 0

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    for fig in _subfigs:
        n += 1
        numrows = math.ceil(len(_subfigs)/float(numcols))
        plt.subplot(numrows, numcols, n)

        # Set labels
        #plt.title(_subfigs[fig]['title'])
        plt.xlabel(_subfigs[fig]['xlabel'], fontsize='small')
        plt.ylabel(_subfigs[fig]['ylabel'], fontsize='small')

        # Fetch datas
        x = np.array(_subfigs[fig]['xdata'])
        y = np.array(_subfigs[fig]['ydata'])

        # Plot
        if _subfigs[fig]['type'] == 'fill':
            plt.fill(x, y, alpha=0.2)
        else:
            plt.plot(x, y)

        # Set axis limits
        try:
            plt.xlim(_subfigs[fig]['xlim'])
        except TypeError:
            pass

        try:
            plt.ylim(_subfigs[fig]['ylim'])
        except TypeError:
            pass

        # Set legend
        if _subfigs[fig]['legend'] != None:
            nc = 1
            if 2 < len(_subfigs[fig]['legend']) <= 4:
                nc = 2
            elif 4 < len(_subfigs[fig]['legend']):
                nc = 3
            plt.legend(_subfigs[fig]['legend'], loc='best', prop={'size':'x-small'},
                       ncol=nc)

        # Set axis fontsize (https://www.cfa.harvard.edu/~jbattat/computer/python/pylab/)
        fontsize = 'x-small'
        ax = plt.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)

    if n > 0:
        if _save:
            plt.savefig(_filename, dpi=300)
        plt.show()

