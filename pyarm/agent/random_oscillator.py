# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import random

class Agent:

    amp = [0.1 for i in range(6)]
    freq = [1. for i in range(6)]
    phase = [0. for i in range(6)]
    off = [0. for i in range(6)]

    def __init__(self):
        pass

    def get_commands(self, angles, velocities, time):
        self.amp = map(update, self.amp)
        self.freq = map(update, self.freq)
        self.off = map(update, self.off)

        return [func(time, self.amp[i], self.freq[i],
                     self.phase[i], self.off[i]) for i in range(6)]

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

    return max(min(commands, 1), 0)

def update(value):
    if bernoulli(0.01):
        return random.random()
    else:
        return value

def bernoulli(p):
    if random.random() <= p:
        return True
    else:
        return False

