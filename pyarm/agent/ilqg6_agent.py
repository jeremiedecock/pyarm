# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.agent import ilqg6 as ilqg
import warnings

EPS = 1e-5
MAXSTEP = 50
DELTA_TIME = None

class Agent:

    cpt = 0

    def __init__(self):
        pass

    def init(self, angles, velocities):
        qs_target = 1.5
        qe_target = 2.1

        init_qs = angles[0]
        init_qe = angles[1]
        init_qps = velocities[0]
        init_qpe = velocities[1]

        print("new target : (", qs_target, ", ", qe_target, ")")
        print("initial state : (", init_qs, ", ", init_qe, ", ", \
                                   init_qps, ", ", init_qpe, ")")

        return_value = ilqg.init(qs_target, qe_target,
                                 DELTA_TIME, EPS, MAXSTEP,
                                 init_qs, init_qe, init_qps, init_qpe)

        if return_value != 0:
            warnings.warn("ILQG : no convergence.")

    def get_commands(self, angles, velocities, time):
        if self.cpt == 0:
            self.init(angles, velocities)

        if self.cpt < MAXSTEP:
            commands = ilqg.getcmd(velocities[0], velocities[1],
                                   angles[0], angles[1])
        else:
            commands = [0., 0., 0., 0., 0., 0.]

        self.cpt += 1

        return commands

