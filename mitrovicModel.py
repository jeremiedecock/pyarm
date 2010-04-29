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

    ### Kambara

    tick_duration = 0.01                       # The state of the arm is updated at every tick_duration time (s)

    theta_min = np.array([-1.75, 0.52])        # Min angles joints (rd) (cf. H.Kambara)
    theta_max = np.array([-0.35, 1.92])        # Max angles joints (rd) (cf. H.Kambara)

    m  = np.array([1.59, 1.44])                # Arm mass   (kg)   [upper, lower]
    la = np.array([0.3,  0.35])                # Arm length (m)    [upper, lower]
    lg = np.array([0.18, 0.21])                # Distance from the center of mass to the joint (m)      [upper, lower]
    I  = np.array([6.78E-2, 7.99E-2])          # Inertia of the link around the joint          (kg.m²)  [upper, lower]

    k  = np.array([3000., 2000., 1400., 1200., 600., 600.])      # Elasticity coefficient            (N/m)
    k0 = np.array([1000., 1000., 600., 600., 300., 300.])        # Intrinsic elasticity  (for u = 0) (N/m)

    b  = np.ones(6) * 100.      # Viscosity coefficient             (N.s/m)
    b0 = np.ones(6) * 50.       # Intrinsic viscosity   (for u = 0) (N.s/m)

    A  = np.array([[4., -4., 0., 0., 2.8, -3.5],[0., 0., 2.5, -2.5, 2.8, -3.5]]).T   # Moment arm (constant matrix) (cm)

    ### Mitrovic

    lm = np.ones(6)                 # TODO : ???
    l0 = np.ones(6) * 10.           # Intrinsic rest length (for u = 0) (cm    ???)TODO : ???
    r  = np.array([-3.491, 3.491, -2.182, 2.182, -5.498, 5.498])    # Constant from the muscle model (...) (cm ???)TODO : ???

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

        # Fetch control signal (motor command) : 6 elements vector (value taken in [0,1])
        u = np.array(input)
        u = u[0:6]
        if DEBUG:
            print "u"
            print u

        # Dynamics ##################################################

        # l : muscle length (cm)
        l = self.lm - np.dot(self.A, self.theta) # TODO
        if DEBUG:
            print "l"
            print l
        
        # dl : muscle length derivative (cm)
        dl = np.dot(-1 * self.A, self.omega) # TODO
        if DEBUG:
            print "dl"
            print dl

        # K : muscle stiffness (N/m)
        K = np.diag(self.k0 + np.dot(self.k, u)) # TODO
        if DEBUG:
            print "K"
            print K

        # B : muscle viscosity (N.s/m)
        B = np.diag(self.b0 + np.dot(self.b, u)) # TODO
        if DEBUG:
            print "B"
            print B

        # lr : muscle rest length (cm)
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
        self.tau = np.dot(-1 * self.A.T, T) # TODO
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
        return self.la.tolist()

