# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm import fig

class MuscleModel:
    """Muscle model.
    
    References :
    [1] W. Li. "Optimal control for biological movement systems".
    PhD thesis, University of California, San Diego, 2006.
    """

    # CONSTANTS ###############################################################

    name = 'Li'

    muscles = ('elbow flexor', 'elbow extensor',
               'shoulder flexor', 'shoulder extensor',
               'double-joints flexor', 'double-joints extensor')

    # Bound values ##############################

    umin, umax = 0, 1

    # Muscle parameters #########################

    # Muscle length when the joint angle = 0 (m) # TODO
    lm0 = np.ones(6) * 0.4

    ###########################################################################

    def __init__(self):
        # Init datas to plot
        fig.subfig('command',
                   title='Command',
                   xlabel='time (s)',
                   ylabel='Command',
                   ylim=[-0.1, 1.1],
                   legend=self.muscles)
        fig.subfig('muscle length',
                   title='Muscle length',
                   xlabel='time (s)',
                   ylabel='Muscle length (m)',
                   legend=self.muscles)

    def compute_torque(self, angles, velocities, command):
        "Compute the torque"

        # Filter command array (6x1) (value taken in [0,1])
        filtered_command = self.filter_command(command)

        # Muscle activation array (6x1)
        muscle_activation = self.muscle_activation(filtered_command)

        # Moment arm array (6x2)
        moment_arm = self.moment_arm(angles)

        # Muscle length array (6x1)
        muscle_length = self.muscle_length(moment_arm, angles)

        # Muscle velocity array (6x1)
        muscle_velocity = self.muscle_velocity(angles, velocities)

        # Muscle tension array (6x1)
        muscle_tension = self.muscle_tension(muscle_length,
                                             muscle_velocity,
                                             muscle_activation)

        # Torque array (2x1)
        torque = np.dot(moment_arm.T, muscle_tension)

        fig.append('command', command)
        fig.append('muscle length', muscle_length)

        return torque


    def filter_command(self, command):
        """Filter commands.

        Return a 6 elements array with value taken in [0, 1]"""
        command = [max(min(float(s), 1.), 0.) for s in command]
        return np.array(command[0:6])

    def muscle_tension(self, ml, mv, ut):
        "Compute the tension of a muscle."
        T = self.fa(ml, ut) * (self.fe(ml) + self.fl(ml) * self.fv(ml, mv))
        return T


    def fa(self, ml, ut):
        "Activation-frequency relationship."
        #print ml
        fa = 1 - np.exp(-(ut / (0.56 * self.nf(ml))) ** self.nf(ml))
        #fa = np.ones(6) * 0.001
        return fa


    def nf(self, ml):
        "???"
        nf = 2.11 + 4.16 * (1./ml - 1.)
        return nf


    def fl(self, ml):
        "Force-length relationship."
        fl = np.exp(-1 * np.abs((ml**1.93 - 1) / 1.03) ** 1.87)
        return fl


    def fv(self, ml, mv):
        "Force-velocity relationship."

        fv = np.zeros(6)
        for i in range(6):
            if mv[i] <= 0:
                fv[i] = (-5.72 - mv[i])\
                        / (-5.72 + mv[i] * (1.38 + 2.09 * ml[i]))
            else:
                fv[i] = (0.62 - (-3.12 + 4.21*ml[i] - 2.67*ml[i]**2) * mv[i])\
                        / (0.62 + mv[i])

        return fv


    def fe(self, ml):
        "Elastic force."
        fe = -0.02 * np.exp(13.8 - 18.7 * ml)
        return fe


    def moment_arm(self, angles):     # TODO
        "Moment arm of a muscle (m)"
        moment_arm  = np.array([[0.04, -0.04, 0.   ,  0.   , 0.028, -0.035],
                                [0.  ,  0.  , 0.025, -0.025, 0.028, -0.035]]).T
        return moment_arm

    def muscle_activation(self, command):  # TODO
        "Muscle activation."
        muscle_activation = command
        return muscle_activation

    def muscle_length(self, moment_arm, angles): # TODO
        "Compute muscle length (m)."
        muscle_length = self.lm0 - np.dot(moment_arm, angles)
        return muscle_length

    def muscle_velocity(self, angles, velocities):
        "Compute muscle contraction velocity (muscle length derivative) (m/s)."
        return - np.dot(self.moment_arm(angles), velocities)

