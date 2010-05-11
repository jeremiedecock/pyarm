#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sys
import getopt


def usage():
    """Print help message"""

    print '''Usage : ./pyarm -m muscle -a arm
    
    A robotic arm model and simulator.

    -m, --muscle
        the muscle model to use (fake, kambara, mitrovic or weiwei)

    -a, --arm
        the arm model to use (kambara, mitrovic or weiwei)

    -n, --nolimit
        ignore joint angles limits

    -r, --realtime
        realtime simulation (framerate dependant)
    '''


def main():
    """The main function"""

    # Parse options ###################
    muscle = 'kambara'
    arm    = 'kambara'
    has_theta_limit = True
    realtime = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'm:a:nrh',
                                   ["muscle=", "arm=", "nolimit", "realtime", "help"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -x not recognized"
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
        elif o in ("-n", "--nolimit"):
            has_theta_limit = False
        elif o in ("-r", "--realtime"):
            realtime = True
        else:
            assert False, "unhandled option"

    if muscle not in ('fake', 'kambara', 'mitrovic', 'weiwei') \
        or arm not in ('kambara', 'mitrovic', 'weiwei'):

        usage()
        sys.exit(2)

    # Main ############################

    if muscle == 'fake':
        import fake_muscle_model as muscle_mod
    elif muscle == 'kambara':
        import kambara_muscle_model as muscle_mod
    elif muscle == 'mitrovic':
        import mitrovic_muscle_model as muscle_mod
    elif muscle == 'weiwei':
        import weiwei_muscle_model as muscle_mod
    else:
        usage()
        sys.exit(2)

    if arm == 'kambara':
        import kambara_arm_model as arm_mod
    elif arm == 'mitrovic':
        import mitrovic_arm_model as arm_mod
    elif arm == 'weiwei':
        import weiwei_arm_model as arm_mod
    else:
        usage()
        sys.exit(2)

    import sfmlGui as view

    arm_model = arm_mod.ArmModel(has_theta_limit)
    muscle_model = muscle_mod.MuscleModel(arm_model.theta)
    gui = view.GUI(muscle_model, arm_model, realtime)
    gui.run()


if __name__ == '__main__':
    main()
    
