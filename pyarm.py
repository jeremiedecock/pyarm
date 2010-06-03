#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sys
import getopt


def usage():
    """Print help message"""

    print '''Usage : ./pyarm [-m MUSCLE] [-a ARM] [-g GUI] [-r]
    
    A robotic arm model and simulator.

    -m, --muscle
        the muscle model to use (fake, kambara, mitrovic or weiwei)

    -a, --arm
        the arm model to use (kambara, mitrovic or weiwei)

    -g, --gui
        the graphical user interface to use (tk, sfml, none)

    -r, --realtime
        realtime simulation (framerate dependant)
    '''


def main():
    """The main function.
    
    The purpose of this function is to get the list of modules to load and
    launch the simulator."""

    # Parse options ###################
    muscle = 'kambara'
    arm    = 'kambara'
    gui    = 'sfml'
    realtime = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                     'm:a:g:rh',
                     ["muscle=", "arm=", "gui=", "realtime", "help"])
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
        elif o in ("-r", "--realtime"):
            realtime = True
        else:
            assert False, "unhandled option"

    if muscle not in ('fake', 'kambara', 'mitrovic', 'weiwei') \
        or arm not in ('kambara', 'mitrovic', 'weiwei') \
        or gui not in ('sfml', 'tk', 'none'):
        usage()
        sys.exit(2)

    # Main ############################

    if muscle == 'fake':
        from model.muscle.forward_dynamics import fake_muscle_model as muscle_mod
    elif muscle == 'kambara':
        from model.muscle.forward_dynamics import kambara_muscle_model as muscle_mod
    elif muscle == 'mitrovic':
        from model.muscle.forward_dynamics import mitrovic_muscle_model as muscle_mod
    elif muscle == 'weiwei':
        from model.muscle.forward_dynamics import weiwei_muscle_model as muscle_mod
    else:
        usage()
        sys.exit(2)

    if arm == 'kambara':
        from model.arm.forward_dynamics import kambara_arm_model as arm_mod
    elif arm == 'mitrovic':
        from model.arm.forward_dynamics import mitrovic_arm_model as arm_mod
    elif arm == 'weiwei':
        from model.arm.forward_dynamics import weiwei_arm_model as arm_mod
    else:
        usage()
        sys.exit(2)

    if gui == 'sfml':
        import sfml_gui as gui_mod
    elif gui == 'tk':
        import tkinter_gui as gui_mod
    elif gui == 'none':
        raise NotImplementedError()
    else:
        usage()
        sys.exit(2)

    arm_model = arm_mod.ArmModel()
    muscle_model = muscle_mod.MuscleModel(arm_model.theta)
    gui = gui_mod.GUI(muscle_model, arm_model, realtime)
    gui.run()


if __name__ == '__main__':
    main()
    
