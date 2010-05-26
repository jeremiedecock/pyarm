# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import math
import fig

class MuscleModel:

    name = 'Weiwei'

    # Bound values for assert
    lm_min,   lm_max   = 0.01, 0.4               # Muscle length (m) (arbitraire)
    dlm_min,  dlm_max  = 0., 1.                 # Muscle length (m) (arbitraire)

    taumin,   taumax   = -200, 200

    _l = None              # Current muscle length (m)

    def __init__(self, theta):
        self._l = self.l(theta)

        # Init datas to plot (title, xlabel, ylabel)
        fig.subfig('length', 'Muscle length', 'time (s)', 'muscle length (m)')
        fig.subfig('torque', 'Torque',        'time (s)', 'Torque (N.m)')

    def update(self, input_signal, theta, dt):

        # Fetch control signal (motor command) : 6 elements vector (value taken in [0,1])
        u = np.array(input_signal)
        u = u[0:6]

        # Dynamics ##################################################

        # tau : total torque (N.m)
        MA = self.MA(theta)
        T = self.T(self.a(u), self.l(theta), self.v(theta, self.vm))
        tau = np.dot(MA,T)

        fig.append('torque', tau)

        assert tau.min() >= self.taumin and tau.max() <= self.taumax, "Total torque"

        return tau


    def T(self, a, l, v):
        """Muscle tension (unitless ???)"""
        T = self.fa(l, a) * (self.fl(l) * self.fv(l, v) + self.fp(l))
        return T

    def MA(self, theta):
        """Moment arm (m ???)"""
        a = 1 # TODO ???
        b = 1 # TODO ???
        c = 1 # TODO ???
        MA = a + b * np.cos(c * theta)
        
        ###
        MA  = np.array([[4., -4., 0., 0., 2.8, -3.5],[0., 0., 2.5, -2.5, 2.8, -3.5]]).T
        ###

        return MA

    # Activation-frequency relationship
    def fa(self, lm, ut):
        fa = 1 - np.exp(-(ut / (0.56 * self.nf(lm))) ** self.nf(lm))
        return fa

    # ???
    def nf(self, lm):
        nf = 2.11 + 4.16 * (1./lm - 1.)
        return nf

    # Force-length relationship
    def fl(self, lm):
        fl = np.exp(-1 * np.abs((lm**1.93 - 1) / 1.03) ** 1.87)
        return fl

    # Force-velocity relationship
    def fv(self, lm, dlm):
        if dlm<=0:
            fv = (-5.72 - dlm) / (-5.72 + dlm * (1.38 + 2.09 * lm))
        else:
            fv = (0.62 - (-3.12 + 4.21 * lm - 2.67 * lm**2) * dlm) / (0.62 + dlm)
        return fv

    # Elastic force
    def fp(self, lm):
        fp = -0.02 * np.exp(13.8 - 18.7 * lm)
        return fp

    def a(self, u):  # TODO u = neural input
        """Muscle activation ([0;1] ???)"""
        a = u # TODO ???
        return a

    def l(self, theta):
        "Compute muscle length (m)."
        l = np.ones(6)
        #l = self.lm - np.dot(self.fa, theta)
        return l

