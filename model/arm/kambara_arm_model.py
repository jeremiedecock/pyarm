# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane).

    References :
    [1] H. Kambara, K. Kim, D. Shin, M. Sato, and Y. Koike.
    "Learning and generation of goal-directed arm reaching from scratch."
    Neural Networks, 22(4):348-361, 2009. 
    """

    # STATE VARIABLES #########################################################

    velocities = None         # Angular velocity (rd/s)
    angles = None             # Joint angle (rd)
    former_time = None        # Time (s)

    # CONSTANTS ###############################################################

    name = 'Kambara'

    legend = ('shoulder', 'elbow')

    # Bound values for assert ###################

    # Min and max joint angles (rd)
    angle_bounds = [
                    # Shoulder
                    {'min': math.radians(-140),
                     'max': math.radians(90)}, 

                    # Elbow
                    {'min': math.radians(0),
                     'max': math.radians(160)}
                   ] 

    # Initial joint angles
    initial_angles = [0., 0.]

    # Arm parameters ############################
    
    shoulder_inertia = 6.78E-2   # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 7.99E-2      # Moment of inertia at elbow join (kg·m²)

    upperarm_mass = 1.59         # Forearm mass (kg)
    forearm_mass = 1.44          # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.35        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    upperarm_cog = 0.18 
    forearm_cog = 0.21 

    # Gravitational acceleration (m/s²)
    g  = 9.8

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

        # Angular acceleration (rad/s²)
        M = self.M(angles)
        C = self.C(angles, velocities)
        G = self.G(angles)
        accelerations = np.dot(np.linalg.inv(M), torque - C - G)
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


    def G(self, theta):
        "Compute gravity force matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.upperarm_mass * self.g * self.upperarm_cog * \
               math.cos(theta[0]) \
               + self.forearm_mass * self.g * \
               (self.upperarm_length * math.cos(\
               theta[0]) + self.forearm_cog * math.cos(theta[0] + theta[1]))
        G[1] = self.forearm_mass * self.g * self.forearm_cog * math.cos(\
               theta[0] + theta[1])

        return G

