# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model.
    
    References :
    [1] W. Li. "Optimal control for biological movement systems".
    PhD thesis, University of California, San Diego, 2006.
    """

    # CONSTANTS ###############################################################

    name = 'Li'

    legend = ('shoulder', 'elbow')

    # Arm parameters ##########################################################

    shoulder_inertia = 2.5E-2    # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 4.5E-2       # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.1           # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.33        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.16 

    # Joint friction matrix
    B = np.array([[0.05, 0.025], [0.025, 0.05]])

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
        B = self.B
        accelerations = np.dot(np.linalg.inv(M),
                               torque - C - np.dot(B, velocities))
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

