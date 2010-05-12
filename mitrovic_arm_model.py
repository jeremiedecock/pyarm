# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np
import fig

class ArmModel:
    """Horizontally planar 2 DoF arm model.
    
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

    # Min and max joint angles (rd) from [6] p.357
    theta_limit = [{'min': math.radians(-90), 'max': math.radians(180)}, 
                   {'min': math.radians(0),   'max': math.radians(180)}] 

    ## Min and max joint angles (rd) (from [3] p.19)
    #theta_limit = [{'min': 2. * math.pi / 9., 'max': 7. * math.pi / 9.}, 
    #               {'min': 2. * math.pi / 9., 'max': 7. * math.pi / 9.}] 

    has_theta_limit = True

    # Initial joint angles : functional standard posture (rd) from [6] p.356-357
    theta_init = [math.radians(45), math.radians(70)]

    # Bound values for assert
    taumin,   taumax   = -200, 200                     # Total torque (N.m) arbitrarily chosen
    alphamin, alphamax = -10E1, 10E1                   # Angular acceleration (rd/s²) arbitrarily chosen
    omegamin, omegamax = -2. * math.pi, 2. * math.pi   # Angular velocity (rd/s) from [3] p.19

    # Arm parameters from from [6] p.356
    # [upper arm, forearm]
    m     = np.array([1.59, 1.44])           # Limb mass (kg)
    L     = np.array([0.3, 0.35])            # Limb length (m)
    Lg    = np.array([0.18, 0.21])           # Distance from the joint center to the center of mass (m)
    I     = np.array([4.77E-2, 5.88E-2])     # Moment of inertia at join point (kg·m²)

    def __init__(self, has_theta_limit):
        self.alpha = np.zeros(2)               # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)               # Angular velocity (rd/s)
        self.theta = np.array(self.theta_init) # Orientation (rd)

        self.has_theta_limit = has_theta_limit
        if self.has_theta_limit:
            self.limit_theta()

        # Init datas to plot (name, title, xlabel, ylabel)
        fig.subfig('alpha',  'Angular acceleration', 'time (s)', 'Angular acceleration (rad/s/s)')
        fig.subfig('omega',  'Angular velocity',     'time (s)', 'Angular velocity (rad/s)')
        fig.subfig('theta',  'Angle',                'time (s)', 'Angle (rad)')

    def update(self, tau, dt):
        """Compute the arm dynamics"""

        # Angular acceleration ########
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)

        # from [1] p.3, [3] p.4 and [6] p.354
        self.alpha = np.dot(np.linalg.inv(M), tau - C) 

        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin \
           and self.alpha.max() <= self.alphamax, "Angular acceleration"

        # Angular velocity ############
        self.omega += self.alpha * dt

        fig.append('omega', self.omega)
        assert self.omega.min() >= self.omegamin \
           and self.omega.max() <= self.omegamax, "Angular velocity"

        # Joint angle #################
        self.theta += self.omega * dt

        if self.has_theta_limit:
            self.limit_theta()

        fig.append('theta', self.theta)

        return self.alpha.tolist(), self.omega.tolist(), (self.theta % (2 * math.pi)).tolist()

    #######################################################

    def M(self, theta):
        """Compute inertia matrix (???)"""
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.L[0]**2
        d2 = self.m[1] * self.L[0] * self.Lg[1]
        d3 = self.I[1]

        M[0, 0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0, 0] = d3 + d2 * math.cos(theta[1])
        M[0, 0] = d3 + d2 * math.cos(theta[1])
        M[1, 1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        if omega.shape != (2,):
            raise TypeError('Omega : shape is ' + str(omega.shape) + ' ((2,) expected)')

        C = np.zeros(2)

        d2 = self.m[1] * self.L[0] * self.Lg[1]

        a1 = np.array([[-2. * omega[1], -1. * omega[1]],
                       [omega[0],    0.]])

        C = d2 * math.sin(theta[1]) * np.dot(a1, omega)

        return C

    def limit_theta(self):
        """Limit theta to respect bound values"""
        for i in range(2):
            if self.theta[i] < self.theta_limit[i]['min']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_limit[i]['min']
            elif self.theta[i] > self.theta_limit[i]['max']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_limit[i]['max']

