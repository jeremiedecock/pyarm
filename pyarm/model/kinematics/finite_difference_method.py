# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np

name = 'Finite difference method'

def forward_kinematics(acceleration, velocity_0, angle_0, delta_time):
    "Compute the forward kinematics with finite difference method."

    # Angular velocity (rad/s) at time_n+1
    velocity_1 = velocity_0 + acceleration * delta_time

    # Joint angle (rad) at time_n+1
    #angle_1 = angle_0 + velocity_0 * delta_time
    angle_1 = angle_0 + velocity_1 * delta_time

    return velocity_1, angle_1
