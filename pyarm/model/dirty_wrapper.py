# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm.model.kinematics import finite_difference_method as kinematics
from pyarm.model.arm import mitrovic_arm_model

# Parameters
DELTA_TIME = 0.01
arm = mitrovic_arm_model.ArmModel()

def compute_next_state(qs, qe, qps, qpe, us, ue):

    # Set state
    arm.angles = np.array([float(qs), float(qe)])
    arm.velocities = np.array([float(qps), float(qpe)])
    torque = np.array([float(us), float(ue)])

    accelerations = arm.compute_acceleration(torque, DELTA_TIME)

    # Forward kinematics
    velocities, angles = kinematics.forward_kinematics(accelerations,
                                                       arm.velocities,
                                                       arm.angles,
                                                       DELTA_TIME)

    return angles[0], angles[1], velocities[0], velocities[1]

