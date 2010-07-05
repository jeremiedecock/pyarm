# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
from model.kinematics import euler as kinematics
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model.
    
    References :
    [0] Djordje Mitrovic
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

    [6] M. Katayama and M. Kawato.
    "Virtual trajectory and stiffness ellipse during multijoint arm movement
    predicted by neural inverse models".
    Biological Cybernetics, 69(5):353-362, 1993.

    [7] Todorov & Li
    """

    # STATE VARIABLES #########################################################

    velocities = None         # Angular velocity (rd/s)
    angles = None             # Joint angle (rd)
    former_time = None        # Time (s)

    # CONSTANTS ###############################################################

    name = 'Mitrovic'

    legend = ('shoulder', 'elbow')

    # Arm parameters from from [6] p.356 ######################################

    shoulder_inertia = 4.77E-2   # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 5.88E-2      # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.44          # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.35        # Forearm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.21 

    ###########################################################################

    def __init__(self):
        self.velocities = np.zeros(2)
        self.angles = np.array(self.initial_angles)

        # TODO
        null, self.velocities, self.angles = self.bound_joint_angles(np.zeros(2),
                                                                    self.velocities,
                                                                    self.angles)

        # Init datas to plot
        fig.subfig('M',
                   title='M',
                   xlabel='time (s)',
                   ylabel='M',
                   legend=('M11', 'M12', 'M21', 'M22'))
        fig.subfig('C',
                   title='C',
                   xlabel='time (s)',
                   ylabel='C',
                   legend=self.legend)
        fig.subfig('angular_acceleration',
                   title='Angular acceleration',
                   xlabel='time (s)',
                   ylabel='Angular acceleration (rad/s/s)',
                   legend=self.legend)
        fig.subfig('angular_velocity',
                   title='Angular velocity',
                   xlabel='time (s)',
                   ylabel='Angular velocity (rad/s)',
                   legend=self.legend)
        fig.subfig('joint_angles',
                   title='Angle',
                   xlabel='time (s)',
                   ylabel='Angle (rad)',
                   legend=self.legend)


    def update(self, torque, dt):
        "Compute the arm dynamics."

        # Load state
        angles = self.angles.copy()
        velocities = self.velocities.copy()

        # Angular accelerations (rad/s²)
        # From [1] p.3, [3] p.4 and [6] p.354
        M = self.M(angles)
        C = self.C(angles, velocities)
        accelerations = np.dot(np.linalg.inv(M), torque - C)
        self.assert_bounds('angular_acceleration', accelerations)

        # Forward kinematics
        accelerations, velocities, angles = kinematics.forward_kinematics(acceleration=accelerations,
                                                                  velocity=velocities,
                                                                  angle=angles,
                                                                  delta_time=dt)
        self.assert_bounds('angular_velocity', velocities)

        # Check collisions
        accelerations, velocities, angles = self.bound_joint_angles(accelerations,
                                                                    velocities,
                                                                    angles)

        # Plot values
        fig.append('M', M.flatten())
        fig.append('C', C)
        fig.append('angular_acceleration', accelerations)
        fig.append('angular_velocity', velocities)
        fig.append('joint_angles', angles)

        # Save state
        self.angles = angles
        self.velocities = velocities

        return accelerations

