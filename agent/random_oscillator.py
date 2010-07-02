# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import random

class Agent:

    amp_s = 0.1
    freq_s = 1.
    phase_s = 0.
    off_s = 0.

    amp_e = 0.2
    freq_e = 1.
    phase_e = math.pi
    off_e = 0.5

    def __init__(self):
        pass

    def get_action(self, alpha=None, omega=None, theta=None, time=None):
        
        if bernoulli(0.01):
            self.amp_s = random.random()

        if bernoulli(0.01):
            self.freq_s = random.random()

        #if bernoulli(0.01):
        #    self.phase_s = random.random() 

        if bernoulli(0.01):
            self.off_s = random.random() * (1 - self.amp_s)
        
        if bernoulli(0.01):
            self.amp_e = random.random()

        if bernoulli(0.01):
            self.freq_e = random.random()

        #if bernoulli(0.01):
        #    self.phase_e = random.random()

        if bernoulli(0.01):
            self.off_e = random.random() * (1 - self.amp_s)

        return (func(time, self.amp_s, self.freq_s, self.phase_s, self.off_s),
                func(time, self.amp_e, self.freq_e, self.phase_e, self.off_e),
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

def bernoulli(p):
    if random.random() <= p:
        return_value = True
    else:
        return_value = False

    return return_value
