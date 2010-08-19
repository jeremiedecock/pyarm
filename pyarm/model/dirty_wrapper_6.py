# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import random
from pyarm.model.kinematics import finite_difference_method as kinematics
from pyarm.model.arm import mitrovic_arm_model
from pyarm.model.muscle import mitrovic_muscle_model

# Parameters
DELTA_TIME = 0.01
arm = mitrovic_arm_model.ArmModel()
muscle = mitrovic_muscle_model.MuscleModel()

def compute_next_state(qs, qe, qps, qpe, u0, u1, u2, u3, u4, u5):

    # Set state
    arm.angles = np.array([float(qs), float(qe)])
    arm.velocities = np.array([float(qps), float(qpe)])
    commands = np.array([float(u0), float(u1), float(u2),
                             float(u3), float(u4), float(u5)])

    #noised_commands = [cmd + random.gauss(0., 0.1) for cmd in commands]
    noised_commands = [cmd + random.gauss(0., 0.5 * cmd) for cmd in commands]

    torque = muscle.compute_torque(arm.angles, arm.velocities, noised_commands)
    accelerations = arm.compute_acceleration(torque, DELTA_TIME)

    # Forward kinematics
    velocities, angles = kinematics.forward_kinematics(accelerations,
                                                       arm.velocities,
                                                       arm.angles,
                                                       DELTA_TIME)

    return angles[0], angles[1], velocities[0], velocities[1]



def compute_acceleration(qs, qe, qps, qpe, u0, u1, u2, u3, u4, u5):

    # Set state
    arm.angles = np.array([float(qs), float(qe)])
    arm.velocities = np.array([float(qps), float(qpe)])
    commands = np.array([float(u0), float(u1), float(u2),
                         float(u3), float(u4), float(u5)])

    torque = muscle.compute_torque(arm.angles, arm.velocities, commands)
    accelerations = arm.compute_acceleration(torque, DELTA_TIME)

    return accelerations[0], accelerations[1]

