# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import math
import fig

class MuscleModel:
    """Muscle model.
    
    References :

    Djordje Mitrovic
    http://www.ipab.informatics.ed.ac.uk/slmc/SLMCpeople/Mitrovic_D.html

    [1] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Adaptive Optimal Control for Redundantly Actuated Arms",
    Proc. Simulation of Adaptive Behavior (SAB), 2008
    
    [2] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Optimal Control with Adaptive Internal Dynamics Models",
    Proc. International Conference on Informatics in Control,
    Automation and Robotics (ICINCO), 2008

    [3] Djordje Mitrovic, Stefan Klanke, Rieko Osu, Mitsuo Kawato,
    and Sethu Vijayakumar, "Impedance Control as an Emergent Mechanism from
    Minimising Uncertainty", under review,  preprint, 2009

    [4] Djordje Mitrovic, Sho Nagashima, Stefan Klanke, Takamitsu Matsubara,
    and Sethu Vijayakumar, "Optimal Feedback Control for Anthropomorphic
    Manipulators", Accepted for ICRA, 2010

    [5] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Exploiting Sensorimotor Stochasticity for Learning Control of Variable
    Impedance Actuators", under review, preprint available soon, 2010

    ---

    This model is based on [6] and [7]

    [6] M. Katayama and M. Kawato (1993), "Virtual trajectory and stiffness
    ellipse during multijoint arm movement predicted by neural inverse models".
    Biological Cybernetics, 69:353-362.

    [7] Todorov & Li
    """

    # STATE VARIABLES #########################################################

    # Muscles length (m)
    muscle_length = None

    # CONSTANTS ###############################################################

    name = 'Mitrovic'

    muscles = ('shoulder flexor', 'shoulder extensor',
               'elbow flexor', 'elbow extensor',
               'double-joints flexor', 'double-joints extensor')

    # Bound values ##############################

    umin, umax = 0, 1

    # Muscle parameters #########################

    # Muscle length when the joint angle = 0 (m)
    lm0 = np.array([0.337, 0.388, 0.375, 0.315, 0.257, 0.256])

    # Intrinsic rest length (for u = 0) (m)
    l0rest = np.array([0.26, 0.26, 0.275, 0.275, 0.237, 0.237])

    # Muscle parameters from [6] p.356-357
    k0 = np.ones(6) * 810.8     # Intrinsic elasticity (for u = 0) (N/m)
    k1 = np.ones(6) * 1621.6    # Elasticity coefficient (N/m)
    b0 = np.ones(6) * 54.1      # Intrinsic viscosity (for u = 0) (N.s/m)
    b1 = np.ones(6) * 108.1     # Viscosity coefficient (N.s/m)

    # Constant from the muscle model (m) from [6] p.357
    l1rest = np.array([-0.03491,  0.03491, -0.02182,
                        0.02182, -0.05498,  0.05498])

    # Moment arm (constant matrix) (m) from [6] p.356
    A = np.array([[ 0.04 ,  0.04 ,  0.   ,  0.   ,  0.028,  0.028],
                  [ 0.   ,  0.   ,  0.025,  0.025,  0.035,  0.035]]).T

    ###########################################################################

    def __init__(self, arm):
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
        "Compute muscle length (m)."
        return self.lm0 - np.dot(self.A, angles)

    def K(self, u):
        "Compute muscle stiffness (N/m)."
        return self.k0 + self.k1 * u

    def B(self, u):
        "Compute muscle viscosity (N.s/m)."
        return self.b0 + self.b1 * u

    def rest_length(self, u):
        "Compute muscle rest length (m)."
        return self.l0rest + self.l1rest * u

    def stretching(self, rest_length, muscle_length):
        "Compute stretching (m)."
        return rest_length - muscle_length

    def elastic_force(self, stiffness, stretching):
        "Compute elastic force (N)."
        return stiffness * stretching

    def viscosity_force(self, viscosity, muscle_velocity):
        "Compute viscosity force (N)."
        return viscosity * muscle_velocity

    def tension(self, elastic_force, viscosity_force):
        "Compute muscle tension (cf. Kelvin-Voight model)."
        return elastic_force - viscosity_force # TODO

    def torque(self, tension):
        "Compute total torque (N.m)."
        return np.dot(-1. * self.A.T, tension)

