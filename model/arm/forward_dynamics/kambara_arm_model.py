# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane).

    References :

    Hiroyuki Kambara

    title={{Learning and generation of goal-directed arm reaching from scratch}},
    author={Kambara, H. and Kim, K. and Shin, D. and Sato, M. and Koike, Y.},
    journal={Neural Networks},
    volume={22},
    number={4},
    pages={348--361},
    year={2009},
    publisher={Elsevier}
    """

    name = 'Kambara'

    alpha = None              # Angular acceleration (rd/s²)
    omega = None              # Angular velocity (rd/s)
    theta = None              # Joint angle (rd)

    theta_bounds = [{'min':-1.75, 'max':0.52},  # Min and max joint angles (rd) (cf. H.Kambara)
    #               {'min':-0.35, 'max':1.92}]
                    {'min':0., 'max':1.92}]

    theta_init = [0., 0.]                      # Orientation (rd)

    # Bound values for assert
    taumin,   taumax   = -200, 200             # Total torque (N.m)
    alphamin, alphamax = -10E1, 10E1           # Angular acceleration (rd/s²)
    omegamin, omegamax = -2. * math.pi, 2. * math.pi   # Angular velocity (rd/s) from [3] p.19

    # Arm parameters ##########################################################
    
    shoulder_inertia = 6.78E-2   # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 7.99E-2      # Moment of inertia at elbow join (kg·m²)

    upperarm_mass = 1.59         # Forearm mass (kg)
    forearm_mass = 1.44          # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.35        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    upperarm_cog = 0.18 
    forearm_cog = 0.21 

    g  = 9.8                                   # Gravitational acceleration (m/s²)


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
        G = self.G(self.theta)

        self.alpha = np.dot(np.linalg.inv(M), tau - C - G)
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

        return self.alpha.tolist(), self.omega.tolist(), (self.theta % (2 * math.pi)).tolist()


    def G(self, theta):
        "Compute gravity force matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.upperarm_mass * self.g * self.upperarm_cog * math.cos(theta[0])  \
               + self.forearm_mass * self.g * (self.upperarm_length * math.cos(theta[0] \
               + self.forearm_cog * math.cos(theta[0] + theta[1])))
        G[1] = self.forearm_mass * self.g * self.forearm_cog * math.cos(theta[0] + theta[1])

        return G

