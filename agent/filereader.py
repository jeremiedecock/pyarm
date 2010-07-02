# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import os

class Agent:

    inputs = []
    cpt = 0

    def __init__(self):
        fd = file('data' + os.sep + 'inputs.dat', 'rU')
        for line in fd.readlines():
            if not line.lstrip().startswith('#'):
                self.inputs.append([float(num) for num in line.split()])
        fd.close()

    def get_action(self, alpha=None, omega=None, theta=None, time=None):
        self.cpt += 1

        if self.cpt < len(self.inputs):
            signal = self.inputs[self.cpt]
        else:
            signal = [0., 0., 0., 0., 0., 0.]

        return signal

