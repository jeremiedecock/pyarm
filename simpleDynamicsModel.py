#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np

DEBUG = True
LIMIT = True     # Considere min/max oridentation ?

class ArmModel:

    former_time = 0.0

    bl        = np.ones(2) * 0.1               # Bones length (m)
    theta_min = np.ones(2) * -1 * math.pi / 2  # Min orientation (rd)
    theta_max = np.ones(2) * math.pi / 2       # Max orientation (rd)

    I     = np.ones(2) * 2.0           # Moment of inertia at join point (kg·m²) TODO

    tau   = np.zeros(2)                # Total torque (N.m)
    alpha = np.zeros(2)                # Angular acceleration (rd/s/s)
    omega = np.zeros(2)                # Angular velocity (rd/s)
    theta = np.zeros(2)                # Orientation (rd)

    def __init__(self):
        pass

    def tick(self, input):
        current_time = time.time()
        delta_time = current_time - self.former_time

        if DEBUG:
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

        if DEBUG:
            print "u"
            print u
        
        # Torque
        self.tau = u * 10
        if DEBUG:
            print "tau"
            print self.tau

        #############################################################

        # Angular acceleration
        self.alpha = self.tau / self.I  # TODO

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

