# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np

_realtime = True
_limit    = True     # Considere min/max oridentation ?

class ArmModel:


    ### Kambara

    delta_time = 0.01                          # The state of the arm is updated at every tick_duration time (s)

    theta_min = np.array([-1.75, 0.52])        # Min angles joints (rd) (cf. H.Kambara)
    theta_max = np.array([-0.35, 1.92])        # Max angles joints (rd) (cf. H.Kambara)

    # Arm dynamics
    m  = np.array([1.59, 1.44])                # Limb mass   (kg)   [upper, lower]
    la = np.array([0.3,  0.35])                # Limb length (m)    [upper, lower]
    lg = np.array([0.18, 0.21])                # Distance from the center of mass to the joint (m)      [upper, lower]
    I  = np.array([6.78E-2, 7.99E-2])          # Rotary inertia of the link around the joint   (kg.m²)  [upper, lower]

    g  = 9.8                                   # Gravitational acceleration (m/s²)

    # Muscles dynamics
    k0 = np.array([1000., 1000., 600., 600., 300., 300.])      # Intrinsic elasticity  (for u = 0) (N/m)
    k1 = np.array([3000., 2000., 1400., 1200., 600., 600.])    # Variation rate of elasticity      (N/m)

    b0 = np.ones(6) * 50.                                      # Intrinsic viscosity   (for u = 0) (N.s/m)
    b1 = np.ones(6) * 100.                                     # Variation rate of viscosity       (N.s/m)

    l0rest = np.ones(6) * 10.                                  # Intrinsic rest length (for u = 0) (cm    ???)TODO : ???
    l1rest = np.ones(6) * 15.                                  # Rest length (cm) # TODO
    ld     = np.array([7.7, 12.8, 10., 4., 2., 1.9])           # ??? (cm) # TODO
    l0     = np.array([7.7, 12.8, 10., 4., 2., 1.9])           # ??? (cm) # TODO

    A  = np.array([[4., -4., 0., 0., 2.8, -3.5],[0., 0., 2.5, -2.5, 2.8, -3.5]]).T   # Moment arm (constant matrix) (cm)

    ###

    def __init__(self):
        self.former_time = 0.0       # Former time (s)

        self.tau   = np.zeros(2)     # Total torque (N.m)
        self.alpha = np.zeros(2)     # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)     # Angular velocity (rd/s)
        self.theta = np.zeros(2)     # Orientation (rd)

        self.length = self.l(self.theta)  # Current muscle length (cm)
        self.v      = np.zeros(6)         # Current muscle contraction velocity (muscle length derivative) (cm/s)

    def tick(self, input):

        # Compute delta time
        current_time = time.time()

        if _realtime:
            self.delta_time = current_time - self.former_time

        # Muscle inverse kinematics #################################

        # Muscle length
        former_length = self.length
        self.length = self.l(self.theta)
        delta_length = self.length - former_length

        # Muscle velocity
        self.v  = delta_length / self.delta_time

        # Dynamics ##################################################

        # tau : total torque (N.m)
        T = self.T(self.u(input), self.length, self.v)
        self.tau = np.dot(self.A.T, T)

        # Angular acceleration
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        G = self.G(self.theta)
        self.alpha = np.dot(np.linalg.inv(M), self.tau - C - G)

        # Kinematics ################################################

        # Angular velocity
        self.omega += self.alpha * self.delta_time

        # Orientation
        self.theta += self.omega * self.delta_time

        if _limit:
            for i in range(2):
                if self.theta[i] < self.theta_min[i]:
                    self.alpha[i] = 0
                    self.omega[i] = 0
                    self.theta[i] = self.theta_min[i]
                elif self.theta[i] > self.theta_max[i]:
                    self.alpha[i] = 0
                    self.omega[i] = 0
                    self.theta[i] = self.theta_max[i]

        # Update clock
        self.former_time = current_time

    def u(self, input):
        """Compute control signal (motor command).

        Return a 6 elements vector (array) with value taken in [0, 1]"""

        u = np.array(input)
        u = u[0:6]

        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        return u

    def l(self, theta):
        """Muscle length (cm)."""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        l = self.l0 - np.dot(self.A, theta) # TODO

        return l
        
    def K(self, u):
        """Muscle stiffness (N/m)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        K = np.diag(self.k0 + self.k1 * u)

        return K

    def B(self, u):
        """Muscle viscosity (N.s/m)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        B = np.diag(self.b0 + self.b1 * u)

        return B

    def lrest(self, u):
        """Muscle rest length (cm)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        lrest = self.l0rest - self.l1rest * u

        return lrest

    def T(self, u, l, v):
        """Muscle tension (cf. Kelvin-Voight model)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')
        if l.shape != (6,): raise TypeError('Muscle length l : shape is ' + str(l.shape) + ' ((6,) expected)')
        if v.shape != (6,): raise TypeError('Muscle contraction velocity v : shape is ' + str(v.shape) + ' ((6,) expected)')

        K = self.K(u)
        B = self.B(u)
        lrest = self.lrest(u)

        T = np.dot(K,(l-lrest)) + np.dot(B,v) # TODO

        return T

    def M(self, theta):
        """Compute inertia matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.la[0]**2
        d2 = self.m[1] * self.la[0] * self.lg[1]
        d3 = self.I[1]

        M[0,0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[1,1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        if omega.shape != (2,): raise TypeError('Omega : shape is ' + str(omega.shape) + ' ((2,) expected)')

        C = np.zeros(2)

        d2 = self.m[1] * self.la[0] * self.lg[1]

        C[0] = -1 * omega[1] * (2. * omega[0] + omega[1]) * d2 * math.sin(theta[1])
        C[1] = omega[0]**2 * d2 * math.sin(theta[1])

        return C

    def G(self, theta):
        """Compute ??? matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.m[0] * self.g * self.lg[0] * math.cos(theta[0]) + self.m[1] * self.g * (self.la[0] * math.cos(theta[0] + self.lg[1] * math.cos(theta[0] + theta[1])))
        G[1] = self.m[1] * self.g * self.lg[1] * math.cos(theta[0] + theta[1])

        return G

    def getTheta(self):
        return (self.theta % (2 * math.pi)).tolist()

    def getOmega(self):
        return self.omega.tolist()

    def getAlpha(self):
        return self.alpha.tolist()

    def getTau(self):
        return self.tau.tolist()

    def getBonesLength(self):
        return self.la.tolist()

