# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    name = 'Fake'

    tau_value = 1

    def __init__(self, theta):
        # Init datas to plot
        fig.subfig('torque',
                   title='Torque',
                   xlabel='time (s)',
                   ylabel='Torque (N.m)',
                   type='fill',
                   legend=('shoulder', 'elbow'))

    def update(self, input_signal, theta, dt):
        """Compute the muscle dynamics"""

        # Control signal
        tau = np.zeros(2)

        i = np.array(input_signal)
        if i[0]:
            tau[0] = self.tau_value
        elif i[1]:
            tau[0] = -self.tau_value

        if i[2]:
            tau[1] = self.tau_value
        elif i[3]:
            tau[1] = -self.tau_value

        fig.append('torque', tau)

        return tau
