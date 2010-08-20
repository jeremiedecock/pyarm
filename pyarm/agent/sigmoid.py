# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math

class Agent:

    def __init__(self):
        pass

    def get_commands(self, angles, velocities, time):
        return (0.,
                0.,
                sigmoid(time, 3.),
                0.,
                0.,
                0.)

def sigmoid(t, offset):
    return 1. / (1. + math.exp(-8. * (t - offset)))

