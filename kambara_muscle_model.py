# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import fig

class MuscleModel:

    name = 'Kambara'

    umin,     umax     = 0, 1
    lmin,     lmax     = 0, 0.5
    lrestmin, lrestmax = 0, 0.5
    # 1 N is the force of Earth's gravity on an object with a mass of about 102 g (1⁄9.81 kg) (such as a small apple).
    # On Earth's surface, a mass of 1 kg exerts a force of approximately 9.8 N [down] (or 1.0 kilogram-force; 1 kgf=9.80665 N by definition). The approximation of 1 kg corresponding to 10 N is sometimes used as a rule of thumb in everyday life and in engineering.
    # The force of Earth's gravity on a human being with a mass of 70 kg is approximately 686 N.
    Tmin,     Tmax     = -200, 200
    taumin,   taumax   = -200, 200

    # Muscles dynamics
    k0 = np.array([1000., 1000., 600., 600., 300., 300.])      # Intrinsic elasticity  (for u = 0) (N/m)
    k1 = np.array([3000., 2000., 1400., 1200., 600., 600.])    # Variation rate of elasticity      (N/m)

    b0 = np.ones(6) * 50.                                      # Intrinsic viscosity   (for u = 0) (N.s/m)
    b1 = np.ones(6) * 100.                                     # Variation rate of viscosity       (N.s/m)

    l0rest = np.ones(6) * 0.1                                  # Intrinsic rest length (for u = 0) (m)TODO : ???
    l1rest = np.ones(6) * 0.15                                 # Rest length (m) # TODO
    ld     = np.array([0.077, 0.128, 0.1, 0.04, 0.02, 0.019])  # ??? (m) # TODO
    l0     = np.array([0.077, 0.128, 0.1, 0.04, 0.02, 0.019])  # Intrinsic length (for u = 0) (m) # TODO

    A  = np.array([[ 0.04 , -0.04 ,  0.   ,  0.   ,  0.028, -0.035],
                   [ 0.   ,  0.   ,  0.025, -0.025,  0.028, -0.035]]).T   # Moment arm (constant matrix) (m)

    length = None        # Current muscle length (m)
    v      = None        # Current muscle contraction velocity (muscle length derivative) (m/s)


    def __init__(self, theta):
        self.length = self.lm(theta)        # Current muscle length (m)
        self.v      = np.zeros(6)          # Current muscle contraction velocity (muscle length derivative) (m/s)

        # Init datas to plot (title, xlabel, ylabel)
        fig.subfig('length', 'Muscle length', 'time (s)', 'muscle length (m)')
        fig.subfig('torque', 'Torque',        'time (s)', 'Torque (N.m)')


    def update(self, input_signal, theta, dt):

        # Muscle inverse kinematics #################################

        # Muscle length
        former_length = self.length
        self.length = self.lm(theta)
        delta_length = self.length - former_length

        fig.append('length', self.length)

        # Muscle velocity
        self.v  = delta_length / dt

        # Dynamics ##################################################

        # tau : total torque (N.m)
        T = self.T(self.u(input_signal), self.length, self.v)
        tau = np.dot(self.A.T, T)

        fig.append('torque', tau)

        assert tau.min() >= self.taumin and tau.max() <= self.taumax, "Total torque"

        return tau


    def u(self, input_signal):
        """Compute control signal (motor command).

        Return a 6 elements vector (array) with value taken in [0, 1]"""

        if isinstance(input_signal, list):
            raise TypeError('Motor command : type is ' + str(type(input_signal)) + ' (list expected)')

        u = np.array(input_signal)
        u = u[0:6]

        assert u.min() >= self.umin and u.max() <= self.umax, 'Motor command'

        return u

    def lm(self, theta):
        """Muscle length (m)."""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        l = self.l0 - np.dot(self.A, theta) # TODO

        assert l.min() >= self.lmin and l.max() <= self.lmax, 'Muscle length'

        return l
        
    def K(self, u):
        """Muscle stiffness (N/m)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        K = self.k0 + self.k1 * u

        return K

    def B(self, u):
        """Muscle viscosity (N.s/m)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        B = self.b0 + self.b1 * u

        return B

    def lr(self, u):
        """Muscle rest length (m)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        lrest = self.l0rest - self.l1rest * u

        assert lrest.min() >= self.lrestmin and lrest.max() <= self.lrestmax, "Muscle rest length"

        return lrest

    def T(self, u, l, v):
        """Muscle tension (cf. Kelvin-Voight model)."""
        if u.shape != (6,): raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')
        if l.shape != (6,): raise TypeError('Muscle length l : shape is ' + str(l.shape) + ' ((6,) expected)')
        if v.shape != (6,): raise TypeError('Muscle contraction velocity v : shape is ' + str(v.shape) + ' ((6,) expected)')

        K = self.K(u)
        B = self.B(u)
        lr = self.lr(u)

        T = K * (l-lr) + B * v

        assert T.min() >= self.Tmin and T.max() <= self.Tmax, 'Muscle Tension'

        return T

