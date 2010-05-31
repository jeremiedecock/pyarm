# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import math
import fig

class MuscleModel:
    """Muscle model.
    
    References :

    Djordje Mitrovic
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

    [6] M. Katayama and M. Kawato (1993), "Virtual trajectory and stiffness
    ellipse during multijoint arm movement predicted by neural inverse models".
    Biological Cybernetics, 69:353-362.

    [7] Todorov & Li
    """

    name = 'Mitrovic'

    _l = None              # Current muscle length (m)

    _lm = np.array([0.337, 0.388, 0.375, 0.315, 0.257, 0.256])   # Muscle length when the joint angle = 0 (m)

    l0 = np.array([0.26, 0.26, 0.275, 0.275, 0.237, 0.237]) # Intrinsic rest length (for u = 0) (m)

    # Muscle parameters from [6] p.356-357
    b  = np.ones(6) * 108.1     # Viscosity coefficient             (N.s/m)
    k  = np.ones(6) * 1621.6    # Elasticity coefficient            (N/m)
    b0 = np.ones(6) * 54.1      # Intrinsic viscosity   (for u = 0) (N.s/m)
    k0 = np.ones(6) * 810.8     # Intrinsic elasticity  (for u = 0) (N/m)

    # Constant from the muscle model (m) from [6] p.357
    r  = np.array([-0.03491,  0.03491, -0.02182,  0.02182, -0.05498,  0.05498])

    # Moment arm (constant matrix) (m) from [6] p.356
    A  = np.array([[ 0.04 ,  0.04 ,  0.   ,  0.   ,  0.028,  0.028],
                   [ 0.   ,  0.   ,  0.025,  0.025,  0.035,  0.035]]).T

    def __init__(self, theta):
        self._l = self.lm(theta)

        # Init datas to plot (title, xlabel, ylabel)
        fig.subfig('length', 'Muscle length', 'time (s)', 'muscle length (m)')
        fig.subfig('torque', 'Torque',        'time (s)', 'Torque (N.m)')

    def update(self, input_signal, theta, dt):

        # Fetch control signal (motor command)
        # 6 elements vector (value taken in [0,1])
        u = np.array(input_signal)[0:6]

        fl = self._l                      # Former muscle length
        self._l = self.lm(theta)
        v  = self.v(self._l, fl, dt)

        K  = self.K(u)
        B  = self.B(u)
        lr = self.lr(u)
        T  = self.T(K, B, lr, self._l, v)

        tau = self.tau(T)

        fig.append('length', self._l)
        fig.append('torque', tau)

        return tau


    def lm(self, theta):
        "Compute muscle length (m)."
        l = self._lm - np.dot(self.A, theta)
        return l

    def v(self, l, fl, dt):
        "Compute muscle contraction velocity (muscle length derivative) (m/s)."
        dl = l - fl
        v  = dl / dt
        return v

    def K(self, u):
        "Compute muscle stiffness (N/m)."
        K = self.k0 + self.k * u
        return K

    def B(self, u):
        "Compute muscle viscosity (N.s/m)."
        B = self.b0 + self.b * u
        return B

    def lr(self, u):
        "Compute muscle rest length (m)."
        lr = self.l0 + self.r * u
        return lr

    def T(self, K, B, lr, l, v):
        "Compute muscle tension (cf. Kelvin-Voight model)."
        T = K * (lr-l) - B * v
        return T

    def tau(self, T):
        "Compute total torque (N.m)."
        tau = np.dot(-1 * self.A.T, T)
        return tau

