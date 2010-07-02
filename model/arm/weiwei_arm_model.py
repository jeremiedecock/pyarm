# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model."""

    name = 'Li'

    legend = ('shoulder', 'elbow')

    # Arm parameters ##########################################################

    shoulder_inertia = 2.5E-2    # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 4.5E-2       # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.1           # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.33        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.16 
    
    B = np.array([[0.05, 0.025], [0.025, 0.05]]) # Joint friction matrix (???)


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
        self.alpha = np.dot(np.linalg.inv(M), tau - C - np.dot(self.B, self.omega))

        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin \
           and self.alpha.max() <= self.alphamax, "Angular acceleration %s" % self.alpha.view()

        # Forward kinematics
        self.alpha, self.omega, self.theta = kinematics.forward_kinematics(acceleration=self.alpha,
                                                               velocity=self.omega,
                                                               angle=self.theta,
                                                               delta_time=dt)
        self.bound_joint_angles()

        fig.append('omega', self.omega)
        fig.append('theta', self.theta)

        assert self.omega.min() >= self.omegamin \
               and self.omega.max() <= self.omegamax, "Angular velocity %s" % self.omega.view()

        return self.alpha.tolist(), self.omega.tolist(), self.theta.tolist()

