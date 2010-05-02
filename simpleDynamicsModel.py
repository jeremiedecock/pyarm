# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np

_realtime = True
_limit    = False     # Considere min/max oridentation ?

class ArmModel:

    former_time = 0.0

    delta_time  = 0.01                       # The state of the arm is updated at every tick_duration time (s)
    
    theta_min = np.array([-1.75, 0.52])      # Min angles joints (rd) (cf. H.Kambara)
    theta_max = np.array([-0.35, 1.92])      # Max angles joints (rd) (cf. H.Kambara)

    la    = np.array([0.3, 0.33])            # Limb length (m)
    m     = np.array([1.4, 1.1])             # Limb mass (kg) [upper, lower]
    s     = np.array([0.11, 0.16])           # Distance from the joint center to the center of mass (m) [upper, lower]
    
    I     = np.array([2.5E-2, 4.5E-2])       # Moment of inertia at join point (kg·m²) TODO
    B     = np.array([[0.05, 0.025],[0.025, 0.05]]) # ???

    tau   = np.zeros(2)                # Total torque (N.m)
    alpha = np.zeros(2)                # Angular acceleration (rd/s/s)
    omega = np.zeros(2)                # Angular velocity (rd/s)
    theta = np.zeros(2)                # Orientation (rd)

    def __init__(self):
        pass

    def tick(self, input):

        current_time = time.time()

        if _realtime:
            self.delta_time = current_time - self.former_time

        if __debug__:
            print "alpha"
            print self.alpha
            print "omega"
            print self.omega
            print "theta"
            print self.theta

        # Control signal
        u = np.zeros(2)

        i = np.array(input)
        if i[0]:
            u[0] = 1
        elif i[3]:
            u[0] = -1

        if i[1]:
            u[1] = 1
        elif i[4]:
            u[1] = -1

        if __debug__:
            print "u"
            print u
        
        # Torque
        self.tau = u
        if __debug__:
            print "tau"
            print self.tau

        #############################################################

        # Angular acceleration
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        self.alpha = np.dot(np.linalg.inv(M), self.tau - C - np.dot(self.B, self.omega))  # TODO

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
        """Compute C matrix"""
        C = np.zeros(2)

        d2 = self.m[1] * self.la[0] * self.s[1]

        C[0] = -1 * omega[1] * (2. * omega[0] + omega[1]) * d2 * math.sin(theta[1])
        C[1] = omega[0]**2 * d2 * math.sin(theta[1])

        return C

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

