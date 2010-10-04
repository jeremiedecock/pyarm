#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sys
import os
import shutil
import getopt

from pyarm import fig
from pyarm import clock as clock_mod

## Lionel's old format
#COMMAND_SLICE = slice(8, 14)
#ANGLES_SLICE = slice(2, 4)
#VELOCITIES_SLICE = slice(0, 2)

# Lionel's new format
COMMAND_SLICE = slice(18, 24)
ANGLES_SLICE = slice(10, 12)
VELOCITIES_SLICE = slice(8, 10)
TARGETS_ANGLES_SLICE = slice(2, 4)

def usage():
    """Print help message"""

    print '''Usage : ./pyarm -d DELTA_TIME [-m MUSCLE] [-a ARM] [-A AGENT] [-g GUI]
                [-D GUI_DELTA_TIME] [-s] [-l] FILENAME
    
    Replay a simulation from FILENAME (experimental).

    -m, --muscle
        the muscle model to use (kambara, mitrovic, li or none)

    -a, --arm
        the arm model to use (kambara, mitrovic, li or sagittal)

    -g, --gui
        the graphical user interface to use (tk, gtk, cairo)

    -d, --deltatime
        timestep value in second (should be near to 0.005 seconds)

    -D, --guideltatime
        set the interval between two display in milliseconds (default = 0.04)

    -s, --screencast
        make a screencast

    -h, --help
        display this help and exit
    '''


def main():
    """The main function.
    
    The purpose of this function is to get the list of modules to load and
    launch the simulator."""

    # Parse options ###########################################################
    muscle = 'none'
    arm = 'li'
    gui = 'tk'
    delta_time = None
    gui_delta_time = 0.04
    screencast = False
    unbounded = False

    log_file = None

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                     'm:a:g:d:D:sh',
                     ["muscle=", "arm=", "gui=", "deltatime=",
                      "guideltatime=", "screencast", "help"])
    except getopt.GetoptError, err:
        # will print something like "option -x not recognized"
        print str(err) 
        usage()
        sys.exit(1)
 
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--muscle"):
            muscle = a
        elif o in ("-a", "--arm"):
            arm = a
        elif o in ("-g", "--gui"):
            gui = a
        elif o in ("-d", "--deltatime"):
            delta_time = float(a)
        elif o in ("-D", "--guideltatime"):
            gui_delta_time = float(a)
        elif o in ("-s", "--screencast"):
            screencast = True
        else:
            assert False, "unhandled option"

    if muscle not in ('none', 'kambara', 'mitrovic', 'li') \
        or arm not in ('kambara', 'mitrovic', 'li', 'sagittal') \
        or gui not in ('tk', 'gtk', 'cairo'):
        usage()
        sys.exit(2)

    try:
        log_file = args[0]
    except IndexError:   # TODO
        usage()
        exit(3)

    # Init ####################################################################

    # Erase the screencast directory
    if screencast:
        shutil.rmtree('screencast', True)
        os.mkdir('screencast')

    # Muscle module
    if muscle == 'none':
        from pyarm.model.muscle import fake_muscle_model as muscle_module
    elif muscle == 'kambara':
        from pyarm.model.muscle import kambara_muscle_model as muscle_module
    elif muscle == 'mitrovic':
        from pyarm.model.muscle import mitrovic_muscle_model as muscle_module
    elif muscle == 'li':
        from pyarm.model.muscle import weiwei_muscle_model as muscle_module
    else:
        usage()
        sys.exit(2)

    # Arm module
    if arm == 'kambara':
        from pyarm.model.arm import kambara_arm_model as arm_module
    elif arm == 'mitrovic':
        from pyarm.model.arm import mitrovic_arm_model as arm_module
    elif arm == 'li':
        from pyarm.model.arm import weiwei_arm_model as arm_module
    elif arm == 'sagittal':
        from pyarm.model.arm import sagittal_arm_model as arm_module
    else:
        usage()
        sys.exit(2)

    # GUI module
    if gui == 'tk':
        from pyarm.gui import tkinter_gui as gui_mod
    elif gui == 'gtk':
        from pyarm.gui import gtk_gui as gui_mod
    elif gui == 'cairo':
        raise NotImplementedError()
    else:
        usage()
        sys.exit(2)

    # Init instances
    arm = arm_module.ArmModel(unbounded)
    muscle = muscle_module.MuscleModel()

    clock = None
    if delta_time is None:
        print "error : -d option isn't set"
        sys.exit(1)
    else:
        clock = clock_mod.SimulationtimeClock(delta_time)

    gui = gui_mod.GUI(muscle, arm, clock, screencast)

    # Miscellaneous initialization
    fig.CLOCK = clock
    former_gui_time = 0
    gui.shoulder_point = [70, 70]
    gui.scale = 1200. # px/m (pixels per meter)

    # The mainloop ############################################################
    fd = file(log_file, 'rU')
    line = fd.readline()

    while gui.running and line != '':       # TODO

        if not line.lstrip().startswith('#'):
            datas = [float(num) for num in line.split()]

            # Update clock
            clock.update()

            # Get input signals
            commands = datas[COMMAND_SLICE]
        
            # Update angles (physics)
            arm.angles = datas[ANGLES_SLICE]
            arm.velocities = datas[VELOCITIES_SLICE]
            torque = [0, 0]
            acceleration = [0, 0]

            # Update target
            gui.target_angle = datas[TARGETS_ANGLES_SLICE]

            # Update GUI
            current_time = clock.time
            if current_time - former_gui_time >= gui_delta_time:
                gui.update(commands, torque, acceleration)
                former_gui_time = current_time

        line = fd.readline()

    fd.close()

    # Quit ####################################################################
    if screencast:
        print "Making screencast..."
        cmd = "ffmpeg2theora -v 7 -f image2 %(path)s/%%05d.%(format)s -o %(path)s/screencast.ogv" % {'path': gui.screencast_path, 'format': gui.screenshot_format}
        print cmd
        os.system(cmd)

if __name__ == '__main__':
    main()

