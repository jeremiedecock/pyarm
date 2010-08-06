# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm import fig

class MuscleModel:

    # CONSTANTS ###############################################################

    name = 'Fake'

    # Muscle parameters #########################

    torque_value = 2.0

    ###########################################################################

    def __init__(self, arm):
        # Init datas to plot
        fig.subfig('input signal',
                   title='Signal',
                   xlabel='time (s)',
                   ylabel='Signal',
                   ylim=[-0.1, 1.1],
                   legend=('shoulder +', 'shoulder -',
                           'elbow +', 'elbow -'))

    def update(self, signal, angles, dt):
        """Compute the muscle dynamics"""

        torque = np.zeros(2)
        torque[0] = (signal[0] - signal[1]) * self.torque_value
        torque[1] = (signal[2] - signal[3]) * self.torque_value

        fig.append('input signal', signal[0:4])

        return torque
