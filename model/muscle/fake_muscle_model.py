# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    name = 'Fake'

    torque_value = 2.0

    def __init__(self, arm):
        # Init datas to plot
        fig.subfig('torque',
                   title='Torque',
                   xlabel='time (s)',
                   ylabel='Torque (N.m)',
                   ylim=[-self.torque_value - 0.1 * self.torque_value,
                          self.torque_value + 0.1 * self.torque_value],
                   legend=('shoulder', 'elbow'))

    def update(self, signal, angles, dt):
        """Compute the muscle dynamics"""

        # Control signal
        torque = np.zeros(2)

        torque[0] = (signal[0] - signal[1]) * self.torque_value
        torque[1] = (signal[2] - signal[3]) * self.torque_value

        fig.append('torque', torque)

        return torque
