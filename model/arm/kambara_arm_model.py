# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane).

    References :

    Hiroyuki Kambara

    title={Learning and generation of goal-directed arm reaching from scratch},
    author={Kambara, H. and Kim, K. and Shin, D. and Sato, M. and Koike, Y.},
    journal={Neural Networks},
    volume={22},
    number={4},
    pages={348--361},
    year={2009},
    publisher={Elsevier}
    """

    name = 'Kambara'

    legend = ('shoulder', 'elbow')

    # Min and max joint angles (rd)
    #theta_bounds = [{'min': math.radians(-50), 'max': math.radians(180)}, 
    #                {'min': math.radians(0),   'max': math.radians(160)}] 
    theta_bounds = [{'min': math.radians(-140), 'max': math.radians(90)}, 
                    {'min': math.radians(0),   'max': math.radians(160)}] 

    # Initial joint angles : functional standard posture (rd) from [6] p.356-357
    theta_init = [0., 0.]

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

    # Gravitational acceleration (m/s²)
    g  = 9.8


    def __init__(self):
        self.alpha = np.zeros(2)               # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)               # Angular velocity (rd/s)
        self.theta = np.array(self.theta_init) # Orientation (rd)

        self.bound_joint_angles()

        # Init datas to plot
        fig.subfig('alpha',
                   title='Angular acceleration',
                   xlabel='time (s)',
                   ylabel='Angular acceleration (rad/s/s)',
                   legend=self.legend)
        fig.subfig('omega',
                   title='Angular velocity',
                   xlabel='time (s)',
                   ylabel='Angular velocity (rad/s)',
                   legend=self.legend)
        fig.subfig('theta',
                   title='Angle',
                   xlabel='time (s)',
                   ylabel='Angle (rad)',
                   legend=self.legend)


    def update(self, tau, dt):
        "Compute the arm dynamics."

        # Angular acceleration (rad/s²)
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        G = self.G(self.theta)

        self.alpha = np.dot(np.linalg.inv(M), tau - C - G)
        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin \
               and self.alpha.max() <= self.alphamax, "Angular acceleration"

        # Forward kinematics
        self.alpha, self.omega, self.theta = kinematics.forward_kinematics(acceleration=self.alpha,
                                                               velocity=self.omega,
                                                               angle=self.theta,
                                                               delta_time=dt)
        self.bound_joint_angles()

        fig.append('omega', self.omega)
        fig.append('theta', self.theta)

        assert self.omega.min() >= self.omegamin \
               and self.omega.max() <= self.omegamax, "Angular velocity"

        return self.alpha.tolist(), self.omega.tolist(), self.theta.tolist()


    def G(self, theta):
        "Compute gravity force matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.upperarm_mass * self.g * self.upperarm_cog * math.cos(theta[0])  \
               + self.forearm_mass * self.g * (self.upperarm_length * math.cos(theta[0]) \
               + self.forearm_cog * math.cos(theta[0] + theta[1]))
        G[1] = self.forearm_mass * self.g * self.forearm_cog * math.cos(theta[0] + theta[1])

        return G

