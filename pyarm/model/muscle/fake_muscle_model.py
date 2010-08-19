# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm import fig

class MuscleModel:
    "Muscle model."

    # CONSTANTS ###############################################################

    name = 'Fake'

    ###########################################################################

    def __init__(self):
        # Init datas to plot
        fig.subfig('command',
                   title='Command',
                   xlabel='time (s)',
                   ylabel='Command',
                   ylim=[-0.1, 1.1])
                   #legend=('shoulder +', 'shoulder -',
                   #        'elbow +', 'elbow -'))

    def compute_torque(self, angles, velocities, command):
        "Compute the torque"

        torque = np.zeros(2)
        if len(command) > 2:
            torque[0] = (command[0] - command[1])
            torque[1] = (command[2] - command[3])
            fig.append('command', command[0:4])
        else:
            torque = np.array(command)
            fig.append('command', command[0:2])

        return torque
