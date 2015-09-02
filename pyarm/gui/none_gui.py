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
    clock = None
    screencast = None

    running = True                                  # TODO
    keyboard_flags = [0., 0., 0., 0., 0., 0.]       # TODO

    def __init__(self, muscle, arm, clock, screencast):
        self.arm = arm
        self.muscle = muscle
        self.clock = clock
        self.screencast = screencast

        print("time      s. angle   e. angle   s. velocity   e. velocity   commands (x6)")

    def update(self, command, torque, acceleration):
        "Redraw the screen."

        print("\r", end=' ')
        print("% 6.2fs  " % self.clock.time, end=' ')
        print("%+1.2frd    %+1.2frd   " % (self.arm.angles[0],
                                           self.arm.angles[1]), end=' ')
        print("%+1.2frd/s     %+1.2frd/s    " % (self.arm.velocities[0],
                                                 self.arm.velocities[1]), end=' ')
        print("%1.2f  %1.2f  %1.2f  %1.2f  %1.2f  %1.2f" % (command[0],
                                                            command[1],
                                                            command[2],
                                                            command[3],
                                                            command[4],
                                                            command[5]), end=' ')
        sys.stdout.flush()

        if self.screencast:
            self.take_a_screenshot()

