# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.model.kinematics import euler as kinematics
from pyarm import fig
import math
import numpy as np
import warnings

ASSERT = False
COLLISION_DETECTION = True

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

    # CONSTANTS ###############################################################

    name = 'Abstract'

    joints = ('shoulder', 'elbow')

    # Bound values ##############################

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
    angle_constraints = [
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

    upperarm_mass = None         # Upperarm mass (kg)
    forearm_mass = None          # Forearm mass (kg)

    upperarm_length = None       # Upperarm length (m)
    forearm_length = None        # Forearm length (m)

    # Distance from the upperarm joint center to the upperarm center of mass (m)
    upperarm_cog = None
    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = None

    shoulder_inertia = None      # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = None         # Moment of inertia at elbow join (kg·m²)

    g = None                     # Gravitational acceleration (m/s²)

    friction_matrix = np.array([[0.05, 0.025], [0.025, 0.05]])

    ###########################################################################

    def __init__(self):
        self.velocities = np.zeros(2)

        angles = np.array(self.initial_angles)
        self.angles = self.constraint_joint_angles(angles)

        # Init datas to plot
        fig.subfig('M',
                   title='M',
                   xlabel='time (s)',
                   ylabel='M',
                   legend=('M11', 'M12', 'M21', 'M22'))
        fig.subfig('C',
                   title='C',
                   xlabel='time (s)',
                   ylabel='C',
                   legend=self.joints)
        fig.subfig('B',
                   title='B',
                   xlabel='time (s)',
                   ylabel='B',
                   legend=self.joints)
        fig.subfig('G',
                   title='G',
                   xlabel='time (s)',
                   ylabel='G',
                   legend=self.joints)
        fig.subfig('N',
                   title='N',
                   xlabel='time (s)',
                   ylabel='Normal force',
                   legend=self.joints)
        fig.subfig('torque',
                   title='Torque',
                   xlabel='time (s)',
                   ylabel='Torque (N.m)',
                   legend=self.joints)
        fig.subfig('tCBG',
                   title='torque - (C + B + G)',
                   xlabel='time (s)',
                   ylabel='Tau - (C + B + G)',
                   legend=self.joints)
        fig.subfig('angular_acceleration',
                   title='Angular acceleration',
                   xlabel='time (s)',
                   ylabel='Acceleration (rad/s/s)',
                   legend=self.joints)
        fig.subfig('angular_velocity',
                   title='Angular velocity',
                   xlabel='time (s)',
                   ylabel='Velocity (rad/s)',
                   legend=self.joints)
        fig.subfig('joint_angles',
                   title='Angle',
                   xlabel='time (s)',
                   ylabel='Angle (rad)',
                   legend=self.joints)


    def update(self, torque, delta_time):
        "Compute the arm dynamics."

        # Load state
        angles = self.angles.copy()
        velocities = self.velocities.copy()

        # Collision detection
        if COLLISION_DETECTION:
            collision_flags = self.collision_detection(angles.copy(),  # TODO
                                                       velocities.copy(),  # TODO
                                                       torque.copy(),  # TODO
                                                       delta_time)

        # Angular acceleration (rad/s²)
        # From [1] p.3, [3] p.4 and [6] p.354
        M = self.M(angles)
        C = self.C(angles, velocities)
        B = self.B(velocities)
        G = self.G(angles)
        normal_force = np.zeros(2)

        if COLLISION_DETECTION:
            filter = [float(flag) for flag in collision_flags]
            normal_force = np.array(filter) * (-torque + C + B + G)  # TODO

        accelerations = np.dot(np.linalg.inv(M), torque - C - B - G + normal_force)  # TODO

        self.assert_bounds('angular_acceleration', accelerations)

        # Forward kinematics
        velocities, angles = kinematics.forward_kinematics(accelerations,
                                                           velocities,
                                                           angles,
                                                           delta_time)
        self.assert_bounds('angular_velocity', velocities)

        if COLLISION_DETECTION:
            filter = [float(not flag) for flag in collision_flags]
            velocities = np.array(filter) * velocities  # TODO
            angles = self.constraint_joint_angles(angles)  # TODO # REMOVE IT #

        # Plot values
        fig.append('M', M.flatten())
        fig.append('C', C)
        fig.append('B', B)
        fig.append('G', G)
        fig.append('N', normal_force)
        fig.append('torque', torque)
        fig.append('tCBG', torque - C - B - G)
        fig.append('angular_acceleration', accelerations)
        fig.append('angular_velocity', velocities)
        fig.append('joint_angles', angles)

        # Save state
        self.angles = angles
        self.velocities = velocities

        return accelerations


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

        C = np.array([-omega[1] * (2. * omega[0] + omega[1]),
                      omega[0]**2] \
                    ) * f2 * math.sin(theta[1])

        return C


    def B(self, omega):
        "Compute joint friction matrix."
        return np.dot(self.friction_matrix, omega)


    def G(self, theta):
        "Compute gravity force matrix."
        if theta.shape != (2,):
            raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.upperarm_mass * self.g * self.upperarm_cog * \
               math.cos(theta[0]) \
               + self.forearm_mass * self.g * \
               (self.upperarm_length * math.cos(\
               theta[0]) + self.forearm_cog * math.cos(theta[0] + theta[1]))
        G[1] = self.forearm_mass * self.g * self.forearm_cog * math.cos(\
               theta[0] + theta[1])

        return G


    def collision_detection(self, angles, velocities, torque, delta_time):
        """Compute angles in order to detect collisions.

        Return True if angle value is out of range (collision) or False
        otherwise."""
        # Angular acceleration (rad/s²)
        # From [1] p.3, [3] p.4 and [6] p.354
        M = self.M(angles)
        C = self.C(angles, velocities)
        B = self.B(velocities)
        G = self.G(angles)
        accelerations = np.dot(np.linalg.inv(M), torque - C - B - G)

        # Forward kinematics
        velocities, angles = kinematics.forward_kinematics(accelerations,
                                                           velocities,
                                                           angles,
                                                           delta_time)

        range_flags = self.assert_joint_angles(angles)

        return [not flag for flag in range_flags]


    def constraint_joint_angles(self, angles):
        "Limit joint angles to respect constraint values."
        for i in range(len(self.joints)):
            angles[i] = max(angles[i], self.angle_constraints[i]['min'])
            angles[i] = min(angles[i], self.angle_constraints[i]['max'])
        return angles


    def assert_joint_angles(self, angles):
        """Check if joint angles to respect constraint values.

        Return True if angles values satisfy constraints or False otherwise."""
        const = self.angle_constraints
        return [const[i]['min'] < angles[i] < const[i]['max'] \
                for i in range(len(self.joints))]


    def assert_bounds(self, name, value):
        """Check if 'value' satisfy minimum and maximum value constraints
        (bounds).

        Arguments
        - name  : the key to reach constraints in 'bounds' dictionary.
        - value : the values to assert (a numpy array).
        """

        if ASSERT:
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

