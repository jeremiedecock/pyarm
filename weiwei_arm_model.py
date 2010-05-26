# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np
import fig

class ArmModel:
    """Horizontally planar 2 DoF arm model."""

    name = 'Weiwei'

    theta_limit = [{'min':-1.75, 'max':0.52},  # Min and max joint angles (rd) (cf. H.Kambara)
                   {'min':-0.35, 'max':1.92}]
    has_theta_limit = True

    theta_init = [0., 0.]                      # Orientation (rd)

    # Bound values for assert
    taumin,   taumax   = -200, 200             # Total torque (N.m)
    alphamin, alphamax = -10E1, 10E1           # Angular acceleration (rd/s²)
    omegamin, omegamax = -10E2, 10E2           # Angular velocity (rd/s)

    # Arm dynamics [upper, lower]
    m     = np.array([1.4, 1.1])               # Limb mass (kg) [upper, lower]
    la    = np.array([0.3, 0.33])              # Limb length (m)
    s     = np.array([0.11, 0.16])             # Distance from the joint center to the center of mass (m) [upper, lower]
    I     = np.array([2.5E-2, 4.5E-2])               # Moment of inertia at join point (kg·m²)
    B     = np.array([[0.05, 0.025], [0.025, 0.05]]) # Joint friction matrix (???)

    def __init__(self, has_theta_limit):
        self.alpha = np.zeros(2)               # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)               # Angular velocity (rd/s)
        self.theta = np.array(self.theta_init) # Orientation (rd)

        self.has_theta_limit = has_theta_limit
        if self.has_theta_limit:
            self.limit_theta()

        # Init datas to plot (name, title, xlabel, ylabel)
        fig.subfig('alpha',  'Angular acceleration', 'time (s)', 'Angular acceleration (rad/s/s)')
        fig.subfig('omega',  'Angular velocity',     'time (s)', 'Angular velocity (rad/s)')
        fig.subfig('theta',  'Angle',                'time (s)', 'Angle (rad)')

    def update(self, tau, dt):
        """Compute the arm dynamics"""

        # Angular acceleration (rad/s²)
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        self.alpha = np.dot(np.linalg.inv(M), tau - C - np.dot(self.B, self.omega))  # TODO

        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin and self.alpha.max() <= self.alphamax, "Angular acceleration"

        # Angular velocity (rad/s) ####
        self.omega += self.alpha * dt

        fig.append('omega', self.omega)
        assert self.omega.min() >= self.omegamin and self.omega.max() <= self.omegamax, "Angular velocity"

        # Joint angle (rad) ###########
        self.theta += self.omega * dt

        if self.has_theta_limit:
            self.limit_theta()

        fig.append('theta', self.theta)

        return self.alpha.tolist(), self.omega.tolist(), (self.theta % (2 * math.pi)).tolist()

    #######################################################

    def M(self, theta):
        """Compute inertia matrix (???)"""
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.la[0]**2
        d2 = self.m[1] * self.la[0] * self.s[1]
        d3 = self.I[1]

        M[0, 0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0, 0] = d3 + d2 * math.cos(theta[1])
        M[0, 0] = d3 + d2 * math.cos(theta[1])
        M[1, 1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        C = np.zeros(2)

        d2 = self.m[1] * self.la[0] * self.s[1]

        C[0] = -1 * omega[1] * (2. * omega[0] + omega[1]) * d2 * math.sin(theta[1])
        C[1] = omega[0]**2 * d2 * math.sin(theta[1])

        return C

    def limit_theta(self):
        """Limit theta to respect bound values"""
        for i in range(2):
            if self.theta[i] < self.theta_limit[i]['min']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_limit[i]['min']
            elif self.theta[i] > self.theta_limit[i]['max']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_limit[i]['max']

