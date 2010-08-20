# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import random

class Agent:

    def __init__(self):
        pass

    def get_commands(self, angles, velocities, time):
        return [random.random() for i in range(6)]

