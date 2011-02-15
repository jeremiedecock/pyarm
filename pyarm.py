#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sys
import os
import shutil
import getopt

from pyarm import fig
from pyarm import clock as clock_mod

VERSION = "0.1.3"

def usage():
    """Print help message"""

    print '''A robotic arm model and simulator.

Usage: ./pyarm [-m MUSCLE] [-a ARM] [-A AGENT] [-g GUI] [-d DELTA_TIME] [-D GUI_DELTA_TIME] [-s] [-l]
    
Options:
    -m, --muscle
        the muscle model to use (kambara, mitrovic, li or none)

    -a, --arm
        the arm model to use (kambara, mitrovic, li or sagittal)

    -A, --agent
        the agent to use (oscillator, random, filereader, sigmoid, heaviside,
        ilqg, none)

    -g, --gui
        the graphical user interface to use (tk, gtk, none)

    -d, --deltatime
        timestep value in second (should be near to 0.005 seconds)
        realtime simulation (eg. framerate dependant simulation) is set if this
        option is omitted

    -D, --guideltatime
        set the interval between two display in milliseconds (default = 0.04)

    -s, --screencast
        make a screencast

    -f, --figures
        save matplotlib figures

    -l, --log
        save numeric values (accelerations, velocities, angles, ...) into a
        file

    -u, --unbounded
        set unbounded joint angles

    -v, --version
        output version information and exit

    -h, --help
        display this help and exit

Examples:
    pyarm -f -l -m mitrovic -d 0.005 -A sigmoid

    pyarm -a sagittal -m kambara -d 0.005 -A sigmoid

Report bugs to <gremy@tuxfamily.org>.
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
    delta_time = None
    gui_delta_time = 0.04
    screencast = False
    save_figures = False
    log = False
    unbounded = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                     'm:a:A:g:d:D:sfluvh',
                     ["muscle=", "arm=", "agent=", "gui=", "deltatime=",
                      "guideltatime=", "screencast", "figures", "log",
                      "unbounded", "version", "help"])
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
        elif o in ("-d", "--deltatime"):
            delta_time = float(a)
        elif o in ("-D", "--guideltatime"):
            gui_delta_time = float(a)
        elif o in ("-s", "--screencast"):
            screencast = True
        elif o in ("-f", "--figures"):
            save_figures = True
        elif o in ("-l", "--log"):
            log = True
        elif o in ("-u", "--unbounded"):
            unbounded = True
        elif o in ("-v", "--version"):
            print 'Pyarm ', VERSION
            print
            print 'Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)'
            print 'This is free software; see the source for copying conditions.',
            print 'There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.'
            sys.exit(0)
        else:
            assert False, "unhandled option"

    if muscle not in ('none', 'kambara', 'mitrovic', 'li') \
        or arm not in ('kambara', 'mitrovic', 'li', 'sagittal') \
        or agent not in ('none', 'oscillator', 'random', 'filereader',
                         'sigmoid', 'heaviside', 'ilqg') \
        or gui not in ('tk', 'gtk', 'cairo', 'none'):
        usage()
        sys.exit(2)

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

    # Agent module
    if agent == 'none':
        agent_module = None
        print 'Press NumKey 1 to 6 to move the arm'
    elif agent == 'oscillator':
        from pyarm.agent import oscillator as agent_module
    elif agent == 'random':
        from pyarm.agent import random_oscillator as agent_module
    elif agent == 'filereader':
        from pyarm.agent import filereader as agent_module
    elif agent == 'sigmoid':
        from pyarm.agent import sigmoid as agent_module
    elif agent == 'heaviside':
        from pyarm.agent import heaviside as agent_module
    elif agent == 'ilqg':
        if muscle == 'none':
            from pyarm.agent import ilqg_agent as agent_module
        else:
            from pyarm.agent import ilqg6_agent as agent_module

        if delta_time is None:
            print("ILQG agent can't be used in realtime mode. " + \
                  "Use -d option to set a delta_time value.")
            sys.exit(3)
        else:
            agent_module.DELTA_TIME = delta_time  ###### TODO !
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
    elif gui == 'none':
        from pyarm.gui import none_gui as gui_mod
    else:
        usage()
        sys.exit(2)

    # Init instances
    arm = arm_module.ArmModel(unbounded)
    muscle = muscle_module.MuscleModel()

    agent = None
    if agent_module != None:
        agent = agent_module.Agent()

    clock = None
    if delta_time is None:
        clock = clock_mod.RealtimeClock()
    else:
        clock = clock_mod.SimulationtimeClock(delta_time)

    gui = gui_mod.GUI(muscle, arm, clock, screencast)

    # Miscellaneous initialization
    fig.CLOCK = clock

    former_gui_time = 0

    fig.subfig('dtime', title='Time', xlabel='time (s)', ylabel='Delta time (s)')

    # The mainloop ############################################################
    while gui.running:

        try:
            # Update clock
            clock.update()
            fig.append('dtime', clock.delta_time)

            # Get input signals
            commands = None
            if agent == None:
                commands = [float(flag) for flag in gui.keyboard_flags]
            else:
                commands = agent.get_commands(arm.angles,
                                              arm.velocities,
                                              clock.time)
        
            # Update angles (physics)
            torque = muscle.compute_torque(arm.angles, arm.velocities, commands)
            acceleration = arm.compute_acceleration(torque, clock.delta_time)

            # Update GUI
            current_time = clock.time
            if current_time - former_gui_time >= gui_delta_time:
                gui.update(commands, torque, acceleration)
                former_gui_time = current_time
        except KeyboardInterrupt:
            # Stop the simulation when Ctrl-c is typed
            gui.running = False

    # Quit ####################################################################
    if screencast:
        print "Making screencast..."
        cmd = "ffmpeg2theora -f image2 %(path)s/%%05d.%(format)s -o %(path)s/screencast.ogv" % {'path': gui.screencast_path, 'format': gui.screenshot_format}
        print cmd
        os.system(cmd)

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
    #parse_arguments()
    #init()
    #run()
    #finalize()

