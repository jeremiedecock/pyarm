# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    name = 'Li'

    legend = ('elbow flexor', 'elbow extensor',
              'shoulder flexor', 'shoulder extensor',
              'double-joints flexor', 'double-joints extensor')

    # Bound values for assert
    ml_min, ml_max = 0.01, 0.6     # Muscle length (m) (arbitraire)
    mv_min, mv_max = 0., 1.        # Muscle velocity (m/s) (arbitraire)

    tau_min, tau_max = -200, 200
    umin,     umax     = 0, 1

    # Muscle length when the joint angle = 0 (m) # TODO
    muscle_length_0 = np.ones(6) * 0.4
    current_muscle_length = None

    def __init__(self, arm):
        moment_arm = self.moment_arm(arm.theta)
        self.current_muscle_length = self.muscle_length(moment_arm, arm.theta)

        # Init datas to plot
        fig.subfig('length',
                   title='Muscle length',
                   xlabel='time (s)',
                   ylabel='muscle length (m)',
                   legend=self.legend)
        fig.subfig('torque',
                   title='Torque',
                   xlabel='time (s)',
                   ylabel='Torque (N.m)',
                   legend=arm.legend)

    def update(self, input_signal, theta, delta_time):

        # Fetch control signal (motor command) :
        # 6 elements vector (value taken in [0,1])
        control_signal = self.u(input_signal)

        # Dynamics ##################################################

        # Control signal array (6x1)
        muscle_activation = self.muscle_activation(control_signal)
        if muscle_activation.shape != (6,):
            raise TypeError('Control_signal : shape is ' \
                            + str(muscle_activation.shape) + ' ((6,) expected)')

        # Former muscle length array (6x1)
        former_muscle_length = self.current_muscle_length

        # Moment arm array (6x2)
        moment_arm = self.moment_arm(theta)
        if moment_arm.shape != (6, 2):
            raise TypeError('Moment_arm : shape is ' \
                            + str(moment_arm.shape) + ' ((6,2) expected)')

        # Muscle length array (6x1)
        self.current_muscle_length = self.muscle_length(moment_arm, theta)
        if self.current_muscle_length.shape != (6,):
            raise TypeError('Muscle_length : shape is ' \
                            + str(self.current_muscle_length.shape) \
                            + ' ((6,) expected)')
        assert self.current_muscle_length.min() >= self.ml_min \
            and self.current_muscle_length.max() <= self.ml_max, 'Muscle length'

        # Muscle velocity array (6x1)
        muscle_velocity = self.muscle_velocity(self.current_muscle_length, \
                                               former_muscle_length, delta_time)
        if muscle_velocity.shape != (6,):
            raise TypeError('Muscle_velocity : shape is ' \
                            + str(muscle_velocity.shape) + ' ((6,) expected)')

        # Muscle tension array (6x1)
        muscle_tension = self.muscle_tension(self.current_muscle_length, \
                                             muscle_velocity, muscle_activation)
        if muscle_tension.shape != (6,):
            raise TypeError('Muscle_tension : shape is ' \
                            + str(muscle_tension.shape) + ' ((6,) expected)')

        # Torque array (2x1)
        torque = np.dot(moment_arm.T, muscle_tension)

        fig.append('length', self.current_muscle_length)
        fig.append('torque', torque)
        assert torque.min() >= self.tau_min \
               and torque.max() <= self.tau_max, "Total torque"

        return torque


    def u(self, input_signal):
        """Compute control signal (motor command).

        Take a list of float.
        Return a 6 elements vector (array) with value taken in [0, 1]"""

        u = np.array(input_signal[0:6])

        assert u.min() >= self.umin and u.max() <= self.umax, 'Motor command'

        return u

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


    def moment_arm(self, theta):     # TODO
        "Moment arm of a muscle (m)"
        moment_arm  = np.array([[0.04, -0.04, 0.   ,  0.   , 0.028, -0.035],
                                [0.  ,  0.  , 0.025, -0.025, 0.028, -0.035]]).T
        return moment_arm

    def muscle_activation(self, control_signal):  # TODO
        "Muscle activation."
        muscle_activation = control_signal
        return muscle_activation

    def muscle_length(self, moment_arm, theta): # TODO
        "Compute muscle length (m)."
        muscle_length = self.muscle_length_0 - np.dot(moment_arm, theta)
        return muscle_length

    def muscle_velocity(self, length, former_length, delta_time): # TODO
        "Compute muscle contraction velocity (muscle length derivative) (m/s)."
        delta_length = length - former_length
        velocity  = delta_length / delta_time
        return velocity

