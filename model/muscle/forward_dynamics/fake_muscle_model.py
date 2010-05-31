# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    name = 'Fake'

    tau_value = 1

    def __init__(self, theta):
        fig.subfig('torque', 'Torque', 'tick number', 'Torque (N.m)', 'fill')

    def update(self, input_signal, theta, dt):
        """Compute the muscle dynamics"""

        # Control signal
        tau = np.zeros(2)

        i = np.array(input_signal)
        if i[0]:
            tau[0] = self.tau_value
        elif i[3]:
            tau[0] = -self.tau_value

        if i[1]:
            tau[1] = self.tau_value
        elif i[4]:
            tau[1] = -self.tau_value

        fig.append('torque', tau)

        return tau
