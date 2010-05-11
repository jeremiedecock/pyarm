# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    taumin,   taumax   = -200, 200

    def __init__(self, theta):
        self.length = self.l(theta)        # Current muscle length (m)
        self.vm     = np.zeros(6)          # Current muscle contraction velocity (muscle length derivative) (m/s)

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
        T = self.A(a, l) * (self.Fl(l) * self.Fv(l, v) + self.Fp(l))
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

    # ???
    def A(self, a, l):
        A = 1 - np.exp(-(a / 0.56 * self.Nf(l)) ** self.Nf(l))
        return A

    # ???
    def Nf(self, l):
        Nf = 2.11 + 4.16 * (1/l - 1)
        return Nf

    # ???
    def Fl(self, l):
        Fl = np.exp(-1 * np.abs((l**1.93 - 1) / 1.03) ** 1.87)
        return Fl

    # ???
    def Fv(self, l, v):
        if v<=0:
            Fv = (-5.72 - v) / (-5.72 + v * (1.38 + 2.09 * l))
        else:
            Fv = (0.62 - (-3.12 + 4.21 * l - 2.67 * l**2) * v) / (0.62 + v)
        return Fv

    # ???
    def Fp(self, l):
        Fp = -0.02 * np.exp(13.8 - 18.7 * l)
        return Fp

    def a(self, u):  # TODO u = neural input
        """Muscle activation ([0;1] ???)"""
        a = u # TODO ???
        return a

    def l(self, theta):
        """Muscle length (m ???)"""
        l = 0.1 # TODO ???
        return l

    def v(self, theta, omega):
        """Muscle velocity (dl/dt ???)"""
        v = 0.1 # TODO ???
        return v

