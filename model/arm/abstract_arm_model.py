# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np
import warnings

class AbstractArmModel:
    """Abstract forward dynamics arm model.

    References :
    [1] M. Katayama and M. Kawato.
    "Virtual trajectory and stiffness ellipse during multijoint arm movement
    predicted by neural inverse models".
    Biological Cybernetics, 69(5):353-362, 1993.
    """

    # STATE VARIABLES #########################################################

    velocities = None         # Angular velocity (rd/s)
    angles = None             # Joint angle (rd)
    former_time = None        # Time (s)

    # CONSTANTS ###############################################################

    name = 'Abstract'

    # Bound values for assert ###################

    bounds = {
              # Angular acceleration (rd/s²)
              'angular_acceleration': {'min': -128. * math.pi,
                                       'max': 128. * math.pi},

              # Angular velocity (rd/s) from [3] p.19
              'angular_velocity': {'min': -8. * math.pi,
                                   'max': 8. * math.pi},
              
              # Total torque (N.m)
              'torque': {'min': -200, 'max': 200}
             }

    # Min and max joint angles (rd)
    angle_bounds = [
                    # Shoulder
                    {'min': math.radians(-30),
                     'max': math.radians(140)}, 

                    # Elbow
                    {'min': math.radians(0),
                     'max': math.radians(160)}
                   ] 

    # Initial joint angles
    # Functional standard posture (rd) from [6] p.356-357
    initial_angles = [math.radians(45), math.radians(70)]


    # Arm parameters ############################

    # Moment of inertia at shoulder join (kg·m²)
    shoulder_inertia = None

    # Moment of inertia at elbow join (kg·m²)
    elbow_inertia = None

    # Forearm mass (kg)
    forearm_mass = None

    # Upperarm length (m)
    upperarm_length = None

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = None

    ###########################################################################

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


    def bound_joint_angles(self, accelerations, velocities, angles):
        "Limit joint angles to respect bound values."
        for i in range(2):
            if angles[i] < self.angle_bounds[i]['min']:
                accelerations[i] = 0
                velocities[i] = 0
                angles[i] = self.angle_bounds[i]['min']
            elif angles[i] > self.angle_bounds[i]['max']:
                accelerations[i] = 0
                velocities[i] = 0
                angles[i] = self.angle_bounds[i]['max']

        return accelerations, velocities, angles


    def assert_bounds(self, name, value):
        """Check if 'value' satisfy minimum and maximum value constraints
        (bounds).

        Arguments
        - name  : the key to reach constraints in 'bounds' dictionary.
        - value : the values to assert (a numpy array).
        """

        if name in self.bounds.keys():
            assert value.min() >= self.bounds[name]['min'] \
               and value.max() <= self.bounds[name]['max'], \
               "%s is out of bounds values :\n" \
               "- expected bounds : [%f, %f]\n" \
               "- actual bounds   : [%f, %f]\n" \
               "\n%s" \
               % (name,
                  self.bounds[name]['min'],
                  self.bounds[name]['max'],
                  value.min(),
                  value.max(),
                  value)
        else:
            warnings.warn("%s is not a valid key" % name)

