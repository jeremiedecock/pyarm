# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm import fig

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

    # CONSTANTS ###############################################################

    name = 'Mitrovic'

    muscles = ('shoulder flexor', 'shoulder extensor',
               'elbow flexor', 'elbow extensor',
               'double-joints flexor', 'double-joints extensor')

    # Bound values ##############################

    umin, umax = 0, 1

    # Muscle parameters #########################

    # Muscle length when joint angles = 0 rad (m) [arbitrary choosen]
    lm0 = np.array([0.15, 0.15, 0.15, 0.15, 0.4, 0.4])

    # Muscle parameters from [6] p.356-357
    k0 = np.ones(6) * 810.8     # Intrinsic elasticity (for u = 0) (N/m)
    k1 = np.ones(6) * 1621.6    # Elasticity coefficient (N/m)
    b0 = np.ones(6) * 54.1      # Intrinsic viscosity (for u = 0) (N.s/m)
    b1 = np.ones(6) * 108.1     # Viscosity coefficient (N.s/m)

    # lm0 - lr0 (m)
    diff_lm0_lr0 = np.array([9.076e-2, -2.793e-2, 5.672e-2,
                             0.436e-2, 14.294e-2, -1.343e-2])
    
    # Intrinsic rest length (for u = 0) (m)
    lr0 = -diff_lm0_lr0 + lm0

    # Variation rate of rest length (m)
    lr1 = np.array([-0.03491,  0.03491, -0.02182,
                     0.02182, -0.05498,  0.05498])

    # Moment arm (constant matrix) (m) from [6] p.356
    A = np.array([[ 0.04 ,  0.04 ,  0.   ,  0.   ,  0.028,  0.028],
                  [ 0.   ,  0.   ,  0.025,  0.025,  0.035,  0.035]]).T

    ###########################################################################

    def __init__(self):
        # Init datas to plot
        fig.subfig('command',
                   title='Command',
                   xlabel='time (s)',
                   ylabel='Command',
                   ylim=[-0.1, 1.1],
                   legend=self.muscles)
        fig.subfig('filtered command',
                   title='Filtered command',
                   xlabel='time (s)',
                   ylabel='command',
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
                   title='Stretching',
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

    def compute_torque(self, angles, velocities, command):
        "Compute the torque"

        filtered_command = self.filter_command(command)

        # Muscle length (m)
        muscle_length = self.muscle_length(angles)

        # Muscle contraction velocity (muscle length derivative) (m/s)
        muscle_velocity = self.muscle_velocity(velocities)

        # Torque (N.m)
        stiffness = self.stiffness(filtered_command)
        viscosity = self.viscosity(filtered_command)
        rest_length = self.rest_length(filtered_command)

        stretching = self.stretching(rest_length, muscle_length)
        elastic_force = self.elastic_force(stiffness, stretching)
        viscosity_force = self.viscosity_force(viscosity, muscle_velocity)
        tension = self.tension(elastic_force, viscosity_force)

        torque = self.torque(tension)

        fig.append('command', command)
        fig.append('filtered command', filtered_command)
        fig.append('stiffness', stiffness)
        fig.append('viscosity', viscosity)
        fig.append('rest length', rest_length)
        fig.append('stretching', stretching)
        fig.append('elastic force', elastic_force)
        fig.append('viscosity force', viscosity_force)
        fig.append('tension', tension)
        fig.append('muscle length', muscle_length)
        fig.append('muscle velocity', muscle_velocity)

        return torque


    def filter_command(self, command):
        """Filter commands.

        Return a 6 elements array with value taken in [0, 1]"""
        command = [max(min(float(s), 1.), 0.) for s in command]
        return np.array(command[0:6])

    def muscle_length(self, angles):
        "Compute muscle length (m)."
        return self.lm0 - np.dot(self.A, angles)

    def muscle_velocity(self, velocities):
        "Compute muscle contraction velocity (muscle length derivative) (m/s)."
        return - np.dot(self.A, velocities)

    def stiffness(self, filtered_command):
        "Compute muscle stiffness (N/m)."
        return self.k0 + self.k1 * filtered_command

    def viscosity(self, filtered_command):
        "Compute muscle viscosity (N.s/m)."
        return self.b0 + self.b1 * filtered_command

    def rest_length(self, filtered_command):
        "Compute muscle rest length (m)."
        return self.lr0 + self.lr1 * filtered_command

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
        return elastic_force - viscosity_force

    def torque(self, tension):
        "Compute total torque (N.m)."
        return np.dot(-1. * self.A.T, tension)

