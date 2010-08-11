#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
from pyarm.model.kinematics import euler as kinematics

DELTA_TIME = 0.01

def main():

    from pyarm.model.arm import mitrovic_arm_model

    arm = mitrovic_arm_model.ArmModel()

    for qs in np.arange(-1., 1.1, 0.5):
        for qe in np.arange(-1., 1.1, 0.5):
            for qps in np.arange(-1., 1.1, 0.5):
                for qpe in np.arange(-1., 1.1, 0.5):
                    for us in np.arange(-1., 1.1, 0.5):
                        for ue in np.arange(-1., 1.1, 0.5):
                            # Set state
                            arm.angles = np.array([qs, qe])
                            arm.velocities = np.array([qps, qpe])
                            torque = np.array([us, ue])

                            accelerations = arm.update(torque, DELTA_TIME)

                            # Forward kinematics
                            velocities, angles = kinematics.forward_kinematics(accelerations,
                                                                               arm.velocities,
                                                                               arm.angles,
                                                                               DELTA_TIME)

                            print qs, "\t",
                            print qe, "\t",
                            print qps, "\t",
                            print qpe, "\t",
                            print us, "\t",
                            print ue, "\t",
                            print angles[0], "\t",
                            print angles[1], "\t",
                            print velocities[0], "\t",
                            print velocities[1]

if __name__ == '__main__':
    main()
