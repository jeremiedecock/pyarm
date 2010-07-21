# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    # STATE VARIABLES #########################################################

    # Muscles length (m)
    muscle_length = None

    # CONSTANTS ###############################################################

    name = 'Kambara'

    muscles = ('shoulder flexor', 'shoulder extensor',
               'elbow flexor', 'elbow extensor',
               'double-joints flexor', 'double-joints extensor')

    # Bound values for assert ###################

    umin,     umax     = 0, 1
    lmin,     lmax     = 0, 0.5
    lrestmin, lrestmax = 0, 0.5
    Tmin,     Tmax     = -200, 200
    taumin,   taumax   = -200, 200

    # Muscle parameters #########################

    # Intrinsic elasticity (for u = 0) (N/m)
    k0 = np.array([1000., 1000., 600., 600., 300., 300.])

    # Variation rate of elasticity (N/m)
    k1 = np.array([3000., 2000., 1400., 1200., 600., 600.])

    # Intrinsic viscosity (for u = 0) (N.s/m)
    b0 = np.ones(6) * 50.

    # Variation rate of viscosity (N.s/m)
    b1 = np.ones(6) * 100.

    # Intrinsic rest length (for u = 0) (m) TODO : ???
    l0rest = np.array([0.26, 0.26, 0.275, 0.275, 0.237, 0.237])

    # Rest length (m) # TODO
    l1rest = np.ones(6) * 0.15

    # ??? (m) # TODO
    #ld = np.array([0.077, 0.128, 0.1, 0.04, 0.02, 0.019])

    # Intrinsic length (for u = 0) (m) # TODO
    lm0 = np.array([0.337, 0.388, 0.375, 0.315, 0.257, 0.256])

    # Moment arm (constant matrix) (m)
    A = np.array([[ 0.04 , -0.04 ,  0.   ,  0.   ,  0.028, -0.035],
                  [ 0.   ,  0.   ,  0.025, -0.025,  0.028, -0.035]]).T

    ###########################################################################

    def __init__(self, arm):
        # Current muscle length (m)
        self.muscle_length = self.lm(arm.angles)

        # Init datas to plot
        fig.subfig('input signal',
                   title='Signal',
                   xlabel='time (s)',
                   ylabel='Signal',
                   ylim=[-0.1, 1.1],
                   legend=self.muscles)
        fig.subfig('u',
                   title='U',
                   xlabel='time (s)',
                   ylabel='u',
                   legend=self.muscles)
        fig.subfig('stiffness',
                   title='Muscle stiffness',
                   xlabel='time (s)',
                   ylabel='Muscle stiffness (N/m)',
                   legend=self.muscles)
        fig.subfig('viscosity',
                   title='Muscle viscosity',
                   xlabel='time (s)',
                   ylabel='Muscle viscosity (N.s/m)',
                   legend=self.muscles)
        fig.subfig('rest length',
                   title='Rest length',
                   xlabel='time (s)',
                   ylabel='Rest length (m)',
                   legend=self.muscles)
        fig.subfig('stretching',
                   title='Stretching (|lr(u)-lm|)',
                   xlabel='time (s)',
                   ylabel='Stretching (m)',
                   legend=self.muscles)
        fig.subfig('elastic force',
                   title='Elastic force',
                   xlabel='time (s)',
                   ylabel='Elastic force (N)',
                   legend=self.muscles)
        fig.subfig('viscosity force',
                   title='Viscosity force',
                   xlabel='time (s)',
                   ylabel='Viscosity force (N)',
                   legend=self.muscles)
        fig.subfig('tension',
                   title='Tension',
                   xlabel='time (s)',
                   ylabel='Tension (N)',
                   legend=self.muscles)
        fig.subfig('muscle length',
                   title='Muscle length',
                   xlabel='time (s)',
                   ylabel='Muscle length (m)',
                   legend=self.muscles)
        fig.subfig('muscle velocity',
                   title='Muscle velocity',
                   xlabel='time (s)',
                   ylabel='Muscle velocity (m/s)',
                   legend=self.muscles)

    def update(self, input_signal, angles, delta_time):

        # Muscle inverse kinematics #################################

        # Muscle length
        former_length = self.muscle_length
        muscle_length = self.lm(angles)
        delta_length = muscle_length - former_length

        # Muscle contraction velocity (muscle length derivative) (m/s)
        muscle_velocity = delta_length / delta_time

        # Dynamics ##################################################

        u = self.u(input_signal)

        stiffness = self.K(u)
        viscosity = self.B(u)
        rest_length = self.rest_length(u)

        stretching = self.stretching(rest_length, muscle_length)
        elastic_force = self.elastic_force(stiffness, stretching)
        viscosity_force = self.viscosity_force(viscosity, muscle_velocity)
        tension = self.tension(elastic_force, viscosity_force)

        torque = self.torque(tension)

        fig.append('input signal', input_signal)
        fig.append('u', u)
        fig.append('stiffness', stiffness)
        fig.append('viscosity', viscosity)
        fig.append('rest length', rest_length)
        fig.append('stretching', stretching)
        fig.append('elastic force', elastic_force)
        fig.append('viscosity force', viscosity_force)
        fig.append('tension', tension)
        fig.append('muscle length', muscle_length)
        fig.append('muscle velocity', muscle_velocity)

        # Save state
        self.muscle_length = muscle_length

        return torque


    def u(self, signal):
        """Compute control signal (motor command).

        Take a list of float.
        Return a 6 elements vector (array) with value taken in [0, 1]"""
        signal = [max(min(s, 1.), 0.) for s in signal]
        return np.array(signal[0:6])

    def lm(self, angles):
        """Muscle length (m)."""
        return self.lm0 - np.dot(self.A, angles) # TODO
        
    def K(self, u):
        """Muscle stiffness (N/m)."""
        return self.k0 + self.k1 * u

    def B(self, u):
        """Muscle viscosity (N.s/m)."""
        return self.b0 + self.b1 * u

    def rest_length(self, u):
        """Muscle rest length (m)."""
        return self.l0rest - self.l1rest * u

    def stretching(self, rest_length, muscle_length):
        "Compute stretching (m)."
        return muscle_length - rest_length

    def elastic_force(self, stiffness, stretching):
        "Compute elastic force (N)."
        return stiffness * stretching

    def viscosity_force(self, viscosity, muscle_velocity):
        "Compute viscosity force (N)."
        return viscosity * muscle_velocity

    def tension(self, elastic_force, viscosity_force):
        "Compute muscle tension (cf. Kelvin-Voight model)."
        return elastic_force + viscosity_force # TODO

    def torque(self, tension):
        "Compute total torque (N.m)."
        return np.dot(self.A.T, tension)

