# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from kambara_arm_model import ArmModel as KambaraArmModel
from model.kinematics import euler as kinematics
import math
import numpy as np
import fig

class ArmModel(KambaraArmModel):
    "Vertically planar 2 DoF arm model (sagittal plane) with gravity and friction."

    name = 'Sagittal'

    legend = ('shoulder', 'elbow')

    B = np.array([[0.2, 0.1], [0.2, 0.1]]) # Joint friction matrix (???)

#    def __init__(self):
#        self.alpha = np.zeros(2)               # Angular acceleration (rd/s²)
#        self.omega = np.zeros(2)               # Angular velocity (rd/s)
#        self.theta = np.array(self.theta_init) # Orientation (rd)
#
#        self.bound_joint_angles()
#
#        # Init datas to plot
#        fig.subfig('alpha',
#                   title='Angular acceleration',
#                   xlabel='time (s)',
#                   ylabel='Angular acceleration (rad/s/s)',
#                   legend=self.legend)
#        fig.subfig('omega',
#                   title='Angular velocity',
#                   xlabel='time (s)',
#                   ylabel='Angular velocity (rad/s)',
#                   legend=self.legend)
#        fig.subfig('theta',
#                   title='Angle',
#                   xlabel='time (s)',
#                   ylabel='Angle (rad)',
#                   legend=self.legend)


    def update(self, tau, dt):
        "Compute the arm dynamics."

        # Angular acceleration (rad/s²)
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        G = self.G(self.theta)
        self.alpha = np.dot(np.linalg.inv(M), tau - C - np.dot(self.B, self.omega) - G)

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

