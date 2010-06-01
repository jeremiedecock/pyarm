# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model."""

    name = 'Weiwei'

    alpha = None              # Angular acceleration (rd/s²)
    omega = None              # Angular velocity (rd/s)
    theta = None              # Joint angle (rd)

    # Bound values for assert
    taumin,   taumax   = -200, 200             # Total torque (N.m)
    alphamin, alphamax = -10E1, 10E1           # Angular acceleration (rd/s²)
    omegamin, omegamax = -2. * math.pi, 2. * math.pi   # Angular velocity (rd/s) from [3] p.19

    # Arm parameters ##########################################################

    shoulder_inertia = 2.5E-2    # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 4.5E-2       # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.1           # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.33        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.16 
    
    B     = np.array([[0.05, 0.025], [0.025, 0.05]]) # Joint friction matrix (???)


    def __init__(self, has_theta_limit):
        self.alpha = np.zeros(2)               # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)               # Angular velocity (rd/s)
        self.theta = np.array(self.theta_init) # Orientation (rd)

        self.has_theta_limit = has_theta_limit
        if self.has_theta_limit:
            self.bound_joint_angles()

        # Init datas to plot (name, title, xlabel, ylabel)
        fig.subfig('alpha',  'Angular acceleration', 'time (s)', 'Angular acceleration (rad/s/s)')
        fig.subfig('omega',  'Angular velocity',     'time (s)', 'Angular velocity (rad/s)')
        fig.subfig('theta',  'Angle',                'time (s)', 'Angle (rad)')


    def update(self, tau, dt):
        "Compute the arm dynamics."

        # Angular acceleration (rad/s²)
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        self.alpha = np.dot(np.linalg.inv(M), tau - C - np.dot(self.B, self.omega))

        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin and self.alpha.max() <= self.alphamax, "Angular acceleration"

        # Angular velocity (rad/s) ####
        self.omega += self.alpha * dt
        fig.append('omega', self.omega)
        assert self.omega.min() >= self.omegamin and self.omega.max() <= self.omegamax, "Angular velocity"

        # Joint angle (rad) ###########
        self.theta += self.omega * dt
        if self.has_theta_limit:
            self.bound_joint_angles()
        fig.append('theta', self.theta)

        return self.alpha.tolist(), self.omega.tolist(), self.theta.tolist()

