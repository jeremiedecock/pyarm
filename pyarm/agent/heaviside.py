# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

class Agent:

    def __init__(self):
        pass

    def get_commands(self, angles, velocities, time):
        return (0.,
                0.,
                heaviside(time, 3.),
                0.,
                0.,
                0.)

def heaviside(t, offset):
    action = 0.
    if t >= offset:
        action = 1.
    return action

