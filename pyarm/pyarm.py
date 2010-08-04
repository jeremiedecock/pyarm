#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sys
import os
import shutil
import getopt
import time
import fig

# The state of the arm is updated at every tick_duration time (s)
DELTA_TIME = 0.005
INIT_TIME = time.time()      # Initial time (s)

def usage():
    """Print help message"""

    print '''Usage : ./pyarm [-m MUSCLE] [-a ARM] [-A AGENT] [-g GUI] [-r] [-s] [-l]
    
    A robotic arm model and simulator.

    -m, --muscle
        the muscle model to use (kambara, mitrovic, li or none)

    -a, --arm
        the arm model to use (kambara, mitrovic, li or sagittal)

    -A, --agent
        the agent to use (oscillator, random, filereader, sigmoid, heaviside, none)

    -g, --gui
        the graphical user interface to use (tk, none)

    -r, --realtime
        realtime simulation (framerate dependant simulation)

    -s, --screencast
        make a screencast

    -f, --figures
        save matplotlib figures

    -l, --log
        save numeric values (accelerations, velocities, angles, ...) into a file
    '''


def main():
    """The main function.
    
    The purpose of this function is to get the list of modules to load and
    launch the simulator."""

    # Parse options ###########################################################
    muscle = 'none'
    arm = 'li'
    agent = 'none'
    gui = 'tk'
    realtime = False
    screencast = False
    save_figures = False
    log = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                     'm:a:A:g:rsflh',
                     ["muscle=", "arm=", "agent=", "gui=", "realtime",
                      "screencast", "figures", "log", "help"])
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
        elif o in ("-A", "--agent"):
            agent = a
        elif o in ("-g", "--gui"):
            gui = a
        elif o in ("-r", "--realtime"):
            realtime = True
        elif o in ("-s", "--screencast"):
            screencast = True
        elif o in ("-f", "--figures"):
            save_figures = True
        elif o in ("-l", "--log"):
            log = True
        else:
            assert False, "unhandled option"

    if muscle not in ('none', 'kambara', 'mitrovic', 'li') \
        or arm not in ('kambara', 'mitrovic', 'li', 'sagittal') \
        or agent not in ('none', 'oscillator', 'random', 'filereader',
                         'sigmoid', 'heaviside') \
        or gui not in ('tk', 'gtk', 'cairo', 'none'):
        usage()
        sys.exit(2)

    # Init ####################################################################

    if muscle == 'none':
        from model.muscle import fake_muscle_model as muscle_mod
    elif muscle == 'kambara':
        from model.muscle import kambara_muscle_model as muscle_mod
    elif muscle == 'mitrovic':
        from model.muscle import mitrovic_muscle_model as muscle_mod
    elif muscle == 'li':
        from model.muscle import weiwei_muscle_model as muscle_mod
    else:
        usage()
        sys.exit(2)

    if arm == 'kambara':
        from model.arm import kambara_arm_model as arm_mod
    elif arm == 'mitrovic':
        from model.arm import mitrovic_arm_model as arm_mod
    elif arm == 'li':
        from model.arm import weiwei_arm_model as arm_mod
    elif arm == 'sagittal':
        from model.arm import sagittal_arm_model as arm_mod
    else:
        usage()
        sys.exit(2)

    if agent == 'none':
        agent_mod = None
    elif agent == 'oscillator':
        from agent import oscillator as agent_mod
    elif agent == 'random':
        from agent import random_oscillator as agent_mod
    elif agent == 'filereader':
        from agent import filereader as agent_mod
    elif agent == 'sigmoid':
        from agent import sigmoid as agent_mod
    elif agent == 'heaviside':
        from agent import heaviside as agent_mod
    else:
        usage()
        sys.exit(2)

    if gui == 'tk':
        from gui import tkinter_gui as gui_mod
    elif gui == 'gtk':
        raise NotImplementedError()
    elif gui == 'cairo':
        raise NotImplementedError()
    elif gui == 'none':
        raise NotImplementedError()
    else:
        usage()
        sys.exit(2)

    arm_model = arm_mod.ArmModel()
    muscle_model = muscle_mod.MuscleModel(arm_model)

    agent = None
    if agent_mod != None:
        agent = agent_mod.Agent()

    gui = gui_mod.GUI(muscle_model, arm_model)

    # Erase the screencast directory
    if screencast:
        shutil.rmtree('screencast', True)
        os.mkdir('screencast')

    # The mainloop ############################################################
    fig.subfig('dtime', title='Time', xlabel='time (s)', ylabel='Delta time (s)')
    former_time = INIT_TIME

    while gui.running:

        # Compute delta time
        current_time = time.time()

        delta_time = None
        if realtime:
            delta_time = current_time - former_time
        else:
            delta_time = DELTA_TIME
    
        fig.append('dtime', delta_time)

        # Get input signals
        input_signal = None
        if agent == None:
            input_signal = [float(flag) for flag in gui.keyboard_flags]
        else:
            elapsed_time = current_time - INIT_TIME
            input_signal = agent.get_action(velocities=arm_model.velocities,
                                            angles=arm_model.angles,
                                            time=elapsed_time)
    
        # Update angles (physics)
        torque = muscle_model.update(input_signal, arm_model.angles, delta_time)
        acceleration = arm_model.update(torque, delta_time)

        # Update clock
        former_time = current_time

        gui.update(input_signal, torque, acceleration)

    # Quit ####################################################################
    if screencast:
        print "Making screencast..."
        os.system("ffmpeg2theora -f image2 %(path)s/%%05d.jpeg" + \
                  "-o %(path)s/screencast.ogv" % {'path': 'screencast'})

    if log:
        print 'Saving log...'
        fig.save_log()

    # Display figures
    if save_figures:
        print 'Saving figures...'
        fig.save_all_figs()
    fig.show()

if __name__ == '__main__':
    main()
    
