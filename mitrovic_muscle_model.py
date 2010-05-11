# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import math
import fig

class MuscleModel:
    """Muscle model.
    
    Djordje Mitrovic :
    http://www.ipab.informatics.ed.ac.uk/slmc/SLMCpeople/Mitrovic_D.html

    [1] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Adaptive Optimal Control for Redundantly Actuated Arms",
    Proc. Simulation of Adaptive Behavior (SAB), 2008
    
    [2] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Optimal Control with Adaptive Internal Dynamics Models",
    Proc. International Conference on Informatics in Control,
    Automation and Robotics (ICINCO), 2008

    [3] Djordje Mitrovic, Stefan Klanke, Rieko Osu, Mitsuo Kawato,
    and Sethu Vijayakumar, "Impedance Control as an Emergent Mechanism from
    Minimising Uncertainty", under review,  preprint, 2009

    [4] Djordje Mitrovic, Sho Nagashima, Stefan Klanke, Takamitsu Matsubara,
    and Sethu Vijayakumar, "Optimal Feedback Control for Anthropomorphic
    Manipulators", Accepted for ICRA, 2010

    [5] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Exploiting Sensorimotor Stochasticity for Learning Control of Variable
    Impedance Actuators", under review, preprint available soon, 2010

    ---

    This model is based on [6] and [7]

    [6] M. Katayama and M. Kawato , "Virtual trajectory and stiffness ellipse
    during multijoint arm movement predicted by neural inverse models",
    journal={Biological Cybernetics},
    volume={69},
    number={5},
    pages={353--362},
    year={1993},
    publisher={Springer}

    [7] Todorov & Li
    """

    length = None        # Current muscle length (m)
    v      = None        # Current muscle contraction velocity (muscle length derivative) (m/s)

    lm = np.ones(6)                 # TODO : ???
    l0 = np.ones(6) * 0.1           # Intrinsic rest length (for u = 0) (m)TODO : ???

    # Min and max joint angles (rd) (from [6] p.357)
    theta_limit = [{'min': math.pi/2., 'max': math.pi}, 
                   {'min': 0., 'max': math.pi}] 
    has_theta_limit = True

    theta_init = [math.pi / 2., math.pi / 2.]  # Orientation (rd) arbitrarily chosen

    # Muscle parameters from from [6] p.356-357
    b  = np.ones(6) * 108.1     # Viscosity coefficient             (N.s/m)
    k  = np.ones(6) * 1621.6    # Elasticity coefficient            (N/m)
    b0 = np.ones(6) * 54.1      # Intrinsic viscosity   (for u = 0) (N.s/m)
    k0 = np.ones(6) * 810.8     # Intrinsic elasticity  (for u = 0) (N/m)
    r  = np.array([-3.491, 3.491, -2.182, 2.182, -5.498, 5.498])    # Constant from the muscle model (cm)
    A  = np.array([[4., 4.,  0.,  0., 2.8, 2.8],
                   [0., 0., 2.5, 2.5, 3.5, 3.5]]).T   # Moment arm (constant matrix) (cm)

    def __init__(self, theta):
        self.length = self.l(theta)        # Current muscle length (m)
        self.v      = np.zeros(6)          # Current muscle contraction velocity (muscle length derivative) (m/s)

        # Init datas to plot (title, xlabel, ylabel)
        fig.subfig('length', 'Muscle length', 'time (s)', 'muscle length (m)')
        fig.subfig('torque', 'Torque',        'time (s)', 'Torque (N.m)')

    def update(self, input_signal, theta, dt):

        # Fetch control signal (motor command) : 6 elements vector (value taken in [0,1])
        u = np.array(input_signal)
        u = u[0:6]

        # Dynamics ##################################################

        self.length = self.l(theta)
        
        # dl : muscle length derivative (cm)
        dl = np.dot(-1 * self.A, self.v) # TODO

        # K : muscle stiffness (N/m)
        K = np.diag(self.k0 + np.dot(self.k, u)) # TODO

        # B : muscle viscosity (N.s/m)
        B = np.diag(self.b0 + np.dot(self.b, u)) # TODO

        # lr : muscle rest length (cm)
        lr = self.l0 + np.dot(self.r, u) # TODO

        # T : muscle tension (cf. Kelvin-Voight model)
        T = np.dot(K,(lr-l)) - np.dot(B,dl) # TODO

        # tau : total torque (N.m)
        tau = np.dot(-1 * self.A.T, T) # TODO
        assert tau[0] > 10 or tau[1] > 10, "Tau > 10"

        return tau


    def l(self, theta):
        """Compute muscle length (cm)"""
        return self.lm - np.dot(self.A, theta) # TODO

