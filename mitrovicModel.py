#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np

DEBUG   = True
ONESHOT = False
LIMIT   = False     # Considere min/max oridentation ?

class ArmModel:

    former_time = 0.0                          # Former time (s)

    bl        = np.ones(2) * 0.1               # Bones length (m)
    theta_min = np.ones(2) * -1 * math.pi / 2  # Min orientation (rd)
    theta_max = np.ones(2) * math.pi / 2       # Max orientation (rd)

    ###

    lm = np.ones(6)                # TODO : ???

    k  = np.ones(6) * 1621.6       # Elasticity coefficient            (N/m   ???)
    b  = np.ones(6) * 108.1        # Viscosity coefficient             (N/s/m ???)
    k0 = np.ones(6) * 810.8        # Intrinsic elasticity  (for u = 0) (N/m   ???)
    b0 = np.ones(6) * 54.1         # Intrinsic viscosity   (for u = 0) (N/s/m ???)
    l0 = np.ones(6)                # Intrinsic rest length (for u = 0) (cm    ???)
    r  = np.array([-3.491, 3.491, -2.182, 2.182, -5.498, 5.498])                   # Constant from the muscle model (...) (cm ???)
    A  = np.array([[4., 4., 0., 0., 2.8, 2.8],[0., 0., 2.5, 2.5, 3.5, 3.5]]).T     # Moment arm (constant matrix)         (???)

    ###

    tau   = np.zeros(2)            # Total torque (N.m)
    alpha = np.zeros(2)            # Angular acceleration (rd/s/s)
    omega = np.zeros(2)            # Angular velocity (rd/s)
    theta = np.zeros(2)            # Orientation (rd)

    def __init__(self):
        pass

    def tick(self, input):

        if DEBUG:
            print "A"
            print self.A
            print "alpha"
            print self.alpha
            print "omega"
            print self.omega
            print "theta"
            print self.theta

        # Compute delta time
        current_time = time.time()
        delta_time = current_time - self.former_time

        # Fetch control signal (motor command)
        u = np.array(input)
        u = u[0:6]
        if DEBUG:
            print "u"
            print u

        # Dynamics ##################################################

        # l : muscle length (m)
        l = self.lm - np.dot(self.A, self.theta)
        if DEBUG:
            print "l"
            print l
        
        # dl : muscle length derivative (m)
        dl = np.dot(-1 * self.A, self.omega)
        if DEBUG:
            print "dl"
            print dl

        # K : muscle stiffness
        K = np.diag(self.k0 + np.dot(self.k, u)) # TODO
        if DEBUG:
            print "K"
            print K

        # B : muscle viscosity
        B = np.diag(self.b0 + np.dot(self.b, u)) # TODO
        if DEBUG:
            print "B"
            print B

        # lr : muscle rest length
        lr = self.l0 + np.dot(self.r, u) # TODO
        if DEBUG:
            print "lr"
            print lr

        # T : muscle tension (cf. Kelvin-Voight model)
        T = np.dot(K,(lr-l)) - np.dot(B,dl) # TODO
        if DEBUG:
            print "T"
            print T

        # tau : total torque (N.m)
        self.tau = np.dot(-1 * self.A.T, T)
        if DEBUG:
            print "tau"
            print self.tau

        # Kinematics ################################################

        # Angular acceleration
        self.alpha = self.tau #/ self.I1  # ??? TODO

        # Angular velocity
        self.omega += self.alpha * delta_time

        # Orientation
        self.theta += self.omega * delta_time

        if LIMIT:
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

        if ONESHOT:
            exit()

    def getTheta(self):
        return (self.theta % (2 * math.pi)).tolist()

    def getOmega(self):
        return self.omega.tolist()

    def getAlpha(self):
        return self.alpha.tolist()

    def getTau(self):
        return self.tau.tolist()

    def getBonesLength(self):
        return self.bl.tolist()

