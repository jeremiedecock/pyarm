#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import os, sys
import getopt

program_name = 'pyarm'


def usage():
    print '''Usage : ./pyarm -m model
    
    A robotic arm model and simulator.

    -m, --model
        the arm model to use (naive, kambara or weiwei)
    '''


def main():
    # Parse options ###################
    model = 'kambara'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'm:h', ["model=", "help"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -x not recognized"
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--model"):
            model = a
        else:
            assert False, "unhandled option"

    if model not in ('kambara', 'naive', 'weiwei'):
        usage()
        sys.exit(2)

    # Main ############################

    import sfmlGui as view

    if model == 'kambara':
        import kambaraModel as model
    elif model == 'naive':
        import simpleDynamicsModel as model
    elif model == 'weiwei':
        import weiweiModel as model
    else:
        usage()
        sys.exit(2)

    armModel = model.ArmModel()
    gui = view.GUI(armModel)
    gui.run()


if __name__ == '__main__':
    main()
    
