# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import os

class Agent:

    inputs = []
    cpt = 0

    def __init__(self):
        try:
            fd = file('commands.dat', 'rU')
            for line in fd.readlines():
                if not line.lstrip().startswith('#'):
                    self.inputs.append([float(num) for num in line.split()])
            fd.close()
        except IOError:
            print()
            print("** Put your controls in the commands.dat file " + \
                  "of the current directory. **")
            print()
            raise

    def get_commands(self, angles, velocities, time):
        self.cpt += 1

        if self.cpt < len(self.inputs):
            command = self.inputs[self.cpt]
        else:
            command = [0. for n in self.inputs[0]]

        return command

