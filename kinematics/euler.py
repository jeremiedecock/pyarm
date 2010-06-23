# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np

name = 'Euler'

def forward_kinematics(acceleration=None,
                       velocity=None,
                       angle=None,
                       delta_time=None):
    "Compute the forward kinematics."

    # Angular velocity (rad/s)
    velocity = velocity + acceleration * delta_time

    # Joint angle (rad)
    angle = angle + velocity * delta_time

    return acceleration, velocity, angle
