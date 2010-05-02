# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np

_realtime = True
_limit    = True                                # Considere min/max oridentation ?

class ArmModel:

    former_time = 0.0                          # Former time (s)
    delta_time  = 0.01                         # The state of the arm is updated at every tick_duration time (s)

    theta_min = np.array([-1.75, 0.52])        # Min angles joints (rd) (cf. H.Kambara)
    theta_max = np.array([-0.35, 1.92])        # Max angles joints (rd) (cf. H.Kambara)

    ### Weiwei

    la    = np.array([0.3, 0.33])              # Limb length (m)
    m     = np.array([1.4, 1.1])               # Limb mass (kg) [upper, lower]
    s     = np.array([0.11, 0.16])             # Distance from the joint center to the center of mass (m) [upper, lower]
    
    I     = np.array([2.5E-2, 4.5E-2])              # Moment of inertia at join point (kg·m²)
    B     = np.array([[0.05, 0.025],[0.025, 0.05]]) # Joint friction matrix (???)

    ###

    tau   = np.zeros(2)            # Total torque (N.m)
    alpha = np.zeros(2)            # Angular acceleration (rd/s/s)
    omega = np.zeros(2)            # Angular velocity (rd/s)
    theta = np.zeros(2)            # Orientation (rd)

    def __init__(self):
        pass

    def tick(self, input):

        # Compute delta time
        current_time = time.time()

        if _realtime:
            self.delta_time = current_time - self.former_time

        # Fetch control signal (motor command) : 6 elements vector (value taken in [0,1])
        u = np.array(input)
        u = u[0:6]

        # Dynamics ##################################################

        # tau : total torque (N.m)
        MA = self.MA(self.theta)
        T = self.T(self.a(u), self.l(self.theta), self.v(self.theta, self.omega))
        self.tau = np.dot(MA,T)

        # Angular acceleration (rad/s/s)
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        self.alpha = np.dot(np.linalg.inv(M), self.tau - C - np.dot(self.B, self.omega))  # TODO

        # Kinematics ################################################

        # Angular velocity (rad/s)
        self.omega += self.alpha * self.delta_time

        # Orientation (rad)
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

    def M(self, theta):
        """Compute inertia matrix (???)"""
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.la[0]**2
        d2 = self.m[1] * self.la[0] * self.s[1]
        d3 = self.I[1]

        M[0,0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[1,1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        C = np.zeros(2)

        d2 = self.m[1] * self.la[0] * self.s[1]

        C[0] = -1 * omega[1] * (2. * omega[0] + omega[1]) * d2 * math.sin(theta[1])
        C[1] = omega[0]**2 * d2 * math.sin(theta[1])

        return C

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

