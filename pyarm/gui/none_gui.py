# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.gui.abstract_gui import AbstractGUI
import sys

# TODO :
# - enable take_a_screenshot with cairo

class GUI(AbstractGUI):
    "Text user interface."

    arm = None
    muscle = None

    running = True                                  # TODO
    keyboard_flags = [0., 0., 0., 0., 0., 0.]       # TODO

    def __init__(self, muscle, arm):
        self.arm = arm
        self.muscle = muscle
        print "s. angle   e. angle   s. velocity   e. velocity   commands (x6)"

    def update(self, command, torque, acceleration):
        "Redraw the screen."

        print "\r",
        print "%+1.2frd    %+1.2frd   " % (self.arm.angles[0],
                                           self.arm.angles[1]),
        print "%+1.2frd/s     %+1.2frd/s    " % (self.arm.velocities[0],
                                                 self.arm.velocities[1]),
        print "%1.2f  %1.2f  %1.2f  %1.2f  %1.2f  %1.2f" % (command[0],
                                                            command[1],
                                                            command[2],
                                                            command[3],
                                                            command[4],
                                                            command[5]),
        sys.stdout.flush()

        ## Update the caneva
        #self.draw_shapes(input_signal)
        #self.take_a_screenshot()

