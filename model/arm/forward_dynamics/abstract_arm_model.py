# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np

class AbstractArmModel:
    """Abstract forward dynamics arm model.

    References :

    [1] M. Katayama and M. Kawato (1993), "Virtual trajectory and stiffness
    ellipse during multijoint arm movement predicted by neural inverse models".
    Biological Cybernetics, 69:353-362.
    """

    name = 'Abstract'

    alpha = None              # Angular acceleration (rd/s²)
    omega = None              # Angular velocity (rd/s)
    theta = None              # Joint angle (rd)

    # Min and max joint angles (rd)
    theta_bounds = [{'min': math.radians(-30), 'max': math.radians(140)}, 
                    {'min': math.radians(0),   'max': math.radians(160)}] 
    #theta_bounds = [{'min': math.radians(-90), 'max': math.radians(180)}, 
    #                {'min': math.radians(0),   'max': math.radians(180)}] 

    # Initial joint angles : functional standard posture (rd) from [6] p.356-357
    theta_init = [math.radians(45), math.radians(70)]

    # Arm parameters ##########################################################

    shoulder_inertia = None   # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = None      # Moment of inertia at elbow join (kg·m²)

    forearm_mass = None       # Forearm mass (kg)

    upperarm_length = None    # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = None 

    def __init__(self):
        raise NotImplementedError("Abstract class.")


    def update(self, torque, delta_time):
        "Compute the arm forward dynamics."
        raise NotImplementedError('Abstract class.')


    def M(self, theta):
        "Compute inertia matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) \
                             + ' ((2,) expected)')
        
        f1 = self.shoulder_inertia + self.elbow_inertia \
             + self.forearm_mass * self.upperarm_length**2
        f2 = self.forearm_mass * self.upperarm_length * self.forearm_cog
        f3 = self.elbow_inertia

        M  = np.zeros([2, 2])
        M[0, 0] = f1 + 2. * f2 * math.cos(theta[1])
        M[0, 1] = f3 + f2 * math.cos(theta[1])
        M[1, 0] = f3 + f2 * math.cos(theta[1])
        M[1, 1] = f3

        return M


    def C(self, theta, omega):
        "Compute centripedal and coriolis forces matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) \
                            + ' ((2,) expected)')
        if omega.shape != (2,):
            raise TypeError('Omega : shape is ' + str(omega.shape) \
                            + ' ((2,) expected)')

        f2 = self.forearm_mass * self.upperarm_length * self.forearm_cog

        C = np.array([-omega[1] * (2. * omega[0] + omega[1]), omega[0]**2]) \
            * f2 * math.sin(theta[1])

        return C


    def bound_joint_angles(self):
        "Limit joint angles to respect bound values."
        for i in range(2):
            if self.theta[i] < self.theta_bounds[i]['min']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_bounds[i]['min']
            elif self.theta[i] > self.theta_bounds[i]['max']:
                self.alpha[i] = 0
                self.omega[i] = 0
                self.theta[i] = self.theta_bounds[i]['max']

