# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math

class Agent:

    def __init__(self):
        pass

    def get_commands(self, angles, velocities, time):

        #f1 = lambda amp, freq, phase, off : amp * math.sin(2.0 * math.pi * freq * time + phase) + off
        #f2 = lambda : amp * math.sin(2.0 * math.pi * freq * time + phase) + off

        return (func(time, 0.3, 1., 0., 0.),
                func(time, 0.3, 1., math.pi, 0.),
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

    commands = amp * math.sin(2.0 * math.pi * freq * time + phase) + off

    return max(min(commands, 1.), 0.)

