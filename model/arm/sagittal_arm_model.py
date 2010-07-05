# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from kambara_arm_model import ArmModel as KambaraArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(KambaraArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane) with gravity and friction.

    References :
    [1] H. Kambara, K. Kim, D. Shin, M. Sato, and Y. Koike.
    "Learning and generation of goal-directed arm reaching from scratch."
    Neural Networks, 22(4):348-361, 2009. 
    """

    # CONSTANTS ###############################################################

    name = 'Sagittal'

    legend = ('shoulder', 'elbow')

    # Arm parameters ############################

    # Joint friction matrix
    B = np.array([[0.2, 0.1], [0.2, 0.1]])

    ###########################################################################

    def update(self, torque, dt):
        "Compute the arm dynamics."

        # Load state
        angles = self.angles.copy()
        velocities = self.velocities.copy()

        # Angular acceleration (rad/s²)
        M = self.M(angles)
        C = self.C(angles, velocities)
        B = self.B
        G = self.G(angles)
        accelerations = np.dot(np.linalg.inv(M),
                               torque - C - np.dot(B, velocities) - G)
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
