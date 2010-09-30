# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import warnings

SUBFIGS = {}
FILE_PREFIX = time.strftime('%d%m%y_%H%M%S_')
FIG_FILENAME = "all_figs.png"
FIG_DIRNAME = "pyarm_figs"
LOG_DIRNAME = "pyarm_logs"
CLOCK = None
SAVE = False

def append(name, y, x=None):
    if name in SUBFIGS:

        if x is None:
            x = CLOCK.time

        #if isinstance(x, numbers.Number):
        if not hasattr(x, 'copy'):
            SUBFIGS[name]['xdata'].append(x)
        #elif isinstance(x, np.ndarray):
        else:
            SUBFIGS[name]['xdata'].append(x.copy())

        #if isinstance(y, numbers.Number):
        if not hasattr(y, 'copy'):
            SUBFIGS[name]['ydata'].append(y)
        #elif isinstance(y, np.ndarray):
        else:
            SUBFIGS[name]['ydata'].append(y.copy())

    else:
        warnings.warn('"' + str(name) +
                      '" has not been declared with fig.subfig(). "'
                      + str(name) + '" is not defined in SUBFIGS.')

def subfig(name, title=None, xlabel='', ylabel='', type='plot', xlim=None,
           ylim=None, legend=None):
    if title is None:
        title = str(name)
    SUBFIGS[name] = {'title':title, 'xlabel':xlabel, 'ylabel':ylabel,
                      'type':type, 'xlim':xlim, 'ylim':ylim, 'legend':legend,
                      'xdata':[], 'ydata':[]}

def save_log():
    try:
        os.mkdir(LOG_DIRNAME)
    except OSError:
        pass

    for fig in SUBFIGS:
        x = SUBFIGS[fig]['xdata']
        y = SUBFIGS[fig]['ydata']
        np.savetxt(os.path.join(LOG_DIRNAME, FILE_PREFIX + str(fig) + '.log'),
                   np.c_[x, y])

def save_fig(name):
    # TODO : factoriser !

    plt.clf()

    # Set labels
    plt.title(SUBFIGS[name]['title'])
    plt.xlabel(SUBFIGS[name]['xlabel'], fontsize='small')
    plt.ylabel(SUBFIGS[name]['ylabel'], fontsize='small')

    # Fetch datas
    x = np.array(SUBFIGS[name]['xdata'])
    y = np.array(SUBFIGS[name]['ydata'])

    # Plot
    plt.plot(x, y)

    # Set axis limits
    try:
        plt.xlim(SUBFIGS[name]['xlim'])
    except TypeError:
        pass

    try:
        plt.ylim(SUBFIGS[name]['ylim'])
    except TypeError:
        pass

    # Set grid
    plt.grid(True)

    # Set legend
    if SUBFIGS[name]['legend'] != None:
        nc = 1
        if 2 < len(SUBFIGS[name]['legend']) <= 4:
            nc = 2
        elif 4 < len(SUBFIGS[name]['legend']):
            nc = 3
        try:
            plt.legend(SUBFIGS[name]['legend'],
                       loc='best',
                       prop={'size':'x-small'},
                       ncol=nc)
        except TypeError:
            # Matplotlib 0.98.1 (Debian Lenny)
            plt.legend(SUBFIGS[name]['legend'],
                       loc='best')

    # Set axis fontsize
    # (https://www.cfa.harvard.edu/~jbattat/computer/python/pylab/)
    fontsize = 'x-small'
    ax = plt.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    plt.savefig(os.path.join(FIG_DIRNAME, FILE_PREFIX + name + '.png'), dpi=300)

    plt.clf()

def save_all_figs():
    try:
        os.mkdir(FIG_DIRNAME)
    except OSError:
        pass

    for fig in SUBFIGS:
        save_fig(fig)

def show(numcols=2):
    n = 0

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    for fig in SUBFIGS:
        n += 1
        numrows = math.ceil(len(SUBFIGS)/float(numcols))
        plt.subplot(numrows, numcols, n)

        # Set labels
        #plt.title(SUBFIGS[fig]['title'])
        plt.xlabel(SUBFIGS[fig]['xlabel'], fontsize='small')
        plt.ylabel(SUBFIGS[fig]['ylabel'], fontsize='small')

        # Fetch datas
        x = np.array(SUBFIGS[fig]['xdata'])
        y = np.array(SUBFIGS[fig]['ydata'])

        # Plot
        plt.plot(x, y)

        # Set axis limits
        try:
            plt.xlim(SUBFIGS[fig]['xlim'])
        except TypeError:
            pass

        try:
            plt.ylim(SUBFIGS[fig]['ylim'])
        except TypeError:
            pass

        # Set legend
        if SUBFIGS[fig]['legend'] != None:
            nc = 1
            if 2 < len(SUBFIGS[fig]['legend']) <= 4:
                nc = 2
            elif 4 < len(SUBFIGS[fig]['legend']):
                nc = 3
            try:
                plt.legend(SUBFIGS[fig]['legend'],
                           loc='best',
                           prop={'size':'x-small'},
                           ncol=nc)
            except TypeError:
                # Matplotlib 0.98.1 (Debian Lenny)
                plt.legend(SUBFIGS[fig]['legend'],
                           loc='best')

        # Set axis fontsize
        # (https://www.cfa.harvard.edu/~jbattat/computer/python/pylab/)
        fontsize = 'x-small'
        ax = plt.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)

    if n > 0:
        if SAVE:
            try:
                os.mkdir(FIG_DIRNAME)
            except OSError:
                pass

            plt.savefig(os.path.join(FIG_DIRNAME, FILE_PREFIX + FIG_FILENAME),
                        dpi=300)
        plt.show()

