# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math


class Agent:

    def __init__(self):
        pass

    def get_action(self, alpha=None, omega=None, theta=None, time=None):

        #f1 = lambda amp, freq, phase, off : amp * math.sin(2.0 * math.pi * freq * time + phase) + off
        #f2 = lambda : amp * math.sin(2.0 * math.pi * freq * time + phase) + off

        return (func(time, 0.1, 1., 0., 0.),
                func(time, 0.2, 1., math.pi, 0.5),
                0.,
                0.,
                0.,
                0.)

def func(time, amp, freq, phase, off):
    """
    amp : Peak amplitude
    freq : Frequency
    phase : Phase (time offset)
    off : Displacement offset
    """

    amp = float(amp)
    freq = float(freq)
    phase = float(phase)
    off = float(off)

    signal = amp * math.sin(2.0 * math.pi * freq * time + phase) + off

    return max(min(signal, 1), 0)

