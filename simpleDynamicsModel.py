#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time

class ArmModel:

    former_time = 0.0

    l1     = 0.1   # Arm length (m)
    l2     = 0.1   # Arm length (m)
    I1     = 2.0   # Moment of inertia at join point (kg·m²)
    I2     = 1.0   # Moment of inertia at join point (kg·m²)
    tau1   = 0.0   # Total torque (N.m)
    tau2   = 0.0   # Total torque (N.m)
    alpha1 = 0.0   # Angular acceleration (rd/s/s)
    alpha2 = 0.0   # Angular acceleration (rd/s/s)
    omega1 = 0.0   # Angular velocity (rd/s)
    omega2 = 0.0   # Angular velocity (rd/s)
    theta1 = 0.0   # Orientation (rd)
    theta2 = 0.0   # Orientation (rd)

    def __init__(self):
        pass

    def tick(self, input):
        current_time = time.time()
        delta_time = current_time - self.former_time

        in1 = 0
        in2 = 0

        if input[0]:
            in1 = 1
        elif input[2]:
            in1 = -1

        if input[1]:
            in2 = 1
        elif input[3]:
            in2 = -1

        # Torque
        self.tau1 = in1 * 10
        self.tau2 = in2 * 10

        # Angular acceleration
        self.alpha1 = self.tau1 / self.I1
        self.alpha2 = self.tau2 / self.I2

        # Angular velocity
        self.omega1 += self.alpha1 * delta_time
        self.omega2 += self.alpha2 * delta_time

        # Orientation
        self.theta1 += self.omega1 * delta_time

        self.theta2 += self.omega1 * delta_time
        self.theta2 += self.omega2 * delta_time

        self.theta1  = self.theta1 % (2 * math.pi)
        self.theta2  = self.theta2 % (2 * math.pi)

        self.former_time = current_time

    def getTheta1(self):
        return self.theta1

    def getTheta2(self):
        return self.theta2

    def getOmega1(self):
        return self.omega1

    def getOmega2(self):
        return self.omega2

    def getAlpha1(self):
        return self.alpha1

    def getAlpha2(self):
        return self.alpha2

    def getTau1(self):
        return self.tau1

    def getTau2(self):
        return self.tau2

    def getL1(self):
        return self.l1

    def getL2(self):
        return self.l2

