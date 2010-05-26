# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np
import fig

class ArmModel:
    """Vertically planar 2 DoF arm model (sagittal plane).

    Hiroyuki Kambara

    title={{Learning and generation of goal-directed arm reaching from scratch}},
    author={Kambara, H. and Kim, K. and Shin, D. and Sato, M. and Koike, Y.},
    journal={Neural Networks},
    volume={22},
    number={4},
    pages={348--361},
    year={2009},
    publisher={Elsevier}
    """

    name = 'Kambara'

    theta_limit = [{'min':-1.75, 'max':0.52},  # Min and max joint angles (rd) (cf. H.Kambara)
    #               {'min':-0.35, 'max':1.92}]
                   {'min':0., 'max':1.92}]
    has_theta_limit = True

    theta_init = [0., 0.]                      # Orientation (rd)

    # Bound values for assert
    taumin,   taumax   = -200, 200             # Total torque (N.m)
    alphamin, alphamax = -10E1, 10E1           # Angular acceleration (rd/s²)
    omegamin, omegamax = -2. * math.pi, 2. * math.pi   # Angular velocity (rd/s) from [3] p.19

    # Arm dynamics [upper, lower]
    m  = np.array([1.59, 1.44])                # Limb mass   (kg)
    L  = np.array([0.3,  0.35])                # Limb length (m)
    lg = np.array([0.18, 0.21])                # Distance from the center of mass to the joint (m)
    I  = np.array([6.78E-2, 7.99E-2])          # Rotary inertia of the link around the joint   (kg.m²)
    g  = 9.8                                   # Gravitational acceleration (m/s²)

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
        G = self.G(self.theta)
        self.alpha = np.dot(np.linalg.inv(M), tau - C - G)

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
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.L[0]**2
        d2 = self.m[1] * self.L[0] * self.lg[1]
        d3 = self.I[1]

        M[0,0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[1,1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        if omega.shape != (2,):
            raise TypeError('Omega : shape is ' + str(omega.shape) + ' ((2,) expected)')

        C = np.zeros(2)

        d2 = self.m[1] * self.L[0] * self.lg[1]

        C[0] = d2 * math.sin(theta[1]) * -1. * omega[1] * (2. * omega[0] + omega[1])
        C[1] = d2 * math.sin(theta[1]) * omega[0]**2

        return C

    def G(self, theta):
        """Compute ??? matrix (???)"""
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.m[0] * self.g * self.lg[0] * math.cos(theta[0])  \
               + self.m[1] * self.g * (self.L[0] * math.cos(theta[0] \
               + self.lg[1] * math.cos(theta[0] + theta[1])))
        G[1] = self.m[1] * self.g * self.lg[1] * math.cos(theta[0] + theta[1])

        return G

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
        
