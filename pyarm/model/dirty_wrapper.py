# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm.model.kinematics import euler as kinematics
from pyarm.model.arm import mitrovic_arm_model

# Parameters
delta_time = 0.01
arm = mitrovic_arm_model.ArmModel()

def test(nb):         # TODO
    return nb ** 2    # TODO

def global_predict(qs, qe, qps, qpe, us, ue):

    # Set state
    arm.angles = np.array([float(qs), float(qe)])
    arm.velocities = np.array([float(qps), float(qpe)])
    torque = np.array([float(us), float(ue)])

    accelerations = arm.update(torque, delta_time)

    # Forward kinematics
    velocities, angles = kinematics.forward_kinematics(accelerations,
                                                       arm.velocities,
                                                       arm.angles,
                                                       delta_time)

    return angles[0], angles[1], velocities[0], velocities[1]

