# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import math
import time
import numpy as np
import fig

_realtime = True
_limit    = True     # Considere min/max oridentation ?

class ArmModel:

    delta_time = 0.01                          # The state of the arm is updated at every tick_duration time (s)

    theta_min = np.array([-1.75, 0.52])        # Min angles joints (rd) (cf. H.Kambara)
    theta_max = np.array([-0.35, 1.92])        # Max angles joints (rd) (cf. H.Kambara)

    umin,     umax     = 0, 1
    lmin,     lmax     = 0, 0.5
    lrestmin, lrestmax = 0, 0.5
    # 1 N is the force of Earth's gravity on an object with a mass of about 102 g (1⁄9.81 kg) (such as a small apple).
    # On Earth's surface, a mass of 1 kg exerts a force of approximately 9.8 N [down] (or 1.0 kilogram-force; 1 kgf=9.80665 N by definition). The approximation of 1 kg corresponding to 10 N is sometimes used as a rule of thumb in everyday life and in engineering.
    # The force of Earth's gravity on a human being with a mass of 70 kg is approximately 686 N.
    Tmin,     Tmax     = -200, 200
    taumin,   taumax   = -200, 200

    alphamin, alphamax = -10E1, 10E1
    omegamin, omegamax = -10E2, 10E2
    thetamin, thetamax = -10E4, 10E4

    # Arm dynamics
    m  = np.array([1.59, 1.44])                # Limb mass   (kg)   [upper, lower]
    la = np.array([0.3,  0.35])                # Limb length (m)    [upper, lower]
    lg = np.array([0.18, 0.21])                # Distance from the center of mass to the joint (m)      [upper, lower]
    I  = np.array([6.78E-2, 7.99E-2])          # Rotary inertia of the link around the joint   (kg.m²)  [upper, lower]

    g  = 9.8                                   # Gravitational acceleration (m/s²)

    # Muscles dynamics
    k0 = np.array([1000., 1000., 600., 600., 300., 300.])      # Intrinsic elasticity  (for u = 0) (N/m)
    k1 = np.array([3000., 2000., 1400., 1200., 600., 600.])    # Variation rate of elasticity      (N/m)

    b0 = np.ones(6) * 50.                                      # Intrinsic viscosity   (for u = 0) (N.s/m)
    b1 = np.ones(6) * 100.                                     # Variation rate of viscosity       (N.s/m)

    l0rest = np.ones(6) * 0.1                                  # Intrinsic rest length (for u = 0) (m    ???)TODO : ???
    l1rest = np.ones(6) * 0.15                                 # Rest length (m) # TODO
    ld     = np.array([0.077, 0.128, 0.1, 0.04, 0.02, 0.019])  # ??? (m) # TODO
    l0     = np.array([0.077, 0.128, 0.1, 0.04, 0.02, 0.019])  # ??? (m) # TODO

    A  = np.array([[ 0.04 , -0.04 ,  0.   ,  0.   ,  0.028, -0.035],
                   [ 0.   ,  0.   ,  0.025, -0.025,  0.028, -0.035]]).T   # Moment arm (constant matrix) (m)


    def __init__(self):
        self.former_time = time.time()     # Former time (s)

        self.tau   = np.zeros(2)           # Total torque (N.m)
        self.alpha = np.zeros(2)           # Angular acceleration (rd/s²)
        self.omega = np.zeros(2)           # Angular velocity (rd/s)
        self.theta = np.zeros(2)           # Orientation (rd)

        self.length = self.l(self.theta)   # Current muscle length (m)
        self.v      = np.zeros(6)          # Current muscle contraction velocity (muscle length derivative) (m/s)

        # Init datas to plot (title, xlabel, ylabel)
        fig.subfig('dtime',  'Time',                 'time (s)', 'delta time (s)')
        fig.subfig('length', 'Muscle length',        'time (s)', 'muscle length (m)')
        fig.subfig('torque', 'Torque',               'time (s)', 'Torque (N.m)')
        fig.subfig('alpha',  'Angular acceleration', 'time (s)', 'Angular acceleration (rad/s/s)')
        fig.subfig('omega',  'Angular velocity',     'time (s)', 'Angular velocity (rad/s)')
        fig.subfig('theta',  'Angle',                'time (s)', 'Angle (rad)')

    def __del__(self):
        fig.show()

    def tick(self, input):

        # Compute delta time
        current_time = time.time()

        if _realtime:
            self.delta_time = current_time - self.former_time

        fig.append('dtime', self.delta_time)

        # Muscle inverse kinematics #################################

        # Muscle length
        former_length = self.length
        self.length = self.l(self.theta)
        delta_length = self.length - former_length

        fig.append('length', self.length)

        # Muscle velocity
        self.v  = delta_length / self.delta_time

        # Dynamics ##################################################

        # tau : total torque (N.m)
        T = self.T(self.u(input), self.length, self.v)
        self.tau = np.dot(self.A.T, T)

        fig.append('torque', self.tau)

        assert self.tau.min() >= self.taumin and self.tau.max() <= self.taumax, "Total torque"

        # Angular acceleration
        M = self.M(self.theta)
        C = self.C(self.theta, self.omega)
        G = self.G(self.theta)
        self.alpha = np.dot(np.linalg.inv(M), self.tau - C - G)

        fig.append('alpha', self.alpha)
        assert self.alpha.min() >= self.alphamin and self.alpha.max() <= self.alphamax, "Angular acceleration"

        # Kinematics ################################################

        # Angular velocity
        self.omega += self.alpha * self.delta_time

        fig.append('omega', self.omega)
        assert self.omega.min() >= self.omegamin and self.omega.max() <= self.omegamax, "Angular velocity"

        # Joint angle
        self.theta += self.omega * self.delta_time

        if _limit:
            for i in range(2):
                if self.theta[i] < self.theta_min[i]:
                    self.alpha[i] = 0
                    self.omega[i] = 0
                    self.theta[i] = self.theta_min[i]
                elif self.theta[i] > self.theta_max[i]:
                    self.alpha[i] = 0
                    self.omega[i] = 0
                    self.theta[i] = self.theta_max[i]

        fig.append('theta', self.theta)
        assert self.theta.min() >= self.thetamin and self.theta.max() <= self.thetamax, "Joint angle"

        # Update clock
        self.former_time = current_time

    def u(self, input):
        """Compute control signal (motor command).

        Return a 6 elements vector (array) with value taken in [0, 1]"""

        if isinstance(input, list):
            raise TypeError('Motor command : type is ' + str(type(x)) + ' (list expected)')

        u = np.array(input)
        u = u[0:6]

        if u.shape != (6,):
            raise TypeError('Motor command : shape is ' + str(u.shape) + ' ((6,) expected)')

        if u.max() > self.umax or u.min() < self.umin:
            raise TypeError('Motor command : values are out of bounds : ' + str(u) + ' ([0,1] expected)')

        return u

    def l(self, theta):
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

    def lrest(self, u):
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
        lrest = self.lrest(u)

        T = K * (l-lrest) + B * v

        assert T.min() >= self.Tmin and T.max() <= self.Tmax, 'Muscle Tension'

        return T

    def M(self, theta):
        """Compute inertia matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        
        M  = np.zeros([2, 2])

        d1 = self.I[0] + self.I[1] + self.m[1] * self.la[0]**2
        d2 = self.m[1] * self.la[0] * self.lg[1]
        d3 = self.I[1]

        M[0,0] = d1 + 2 * d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[0,0] = d3 + d2 * math.cos(theta[1])
        M[1,1] = d3

        return M

    def C(self, theta, omega):
        """Compute centripedal and coriolis forces matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')
        if omega.shape != (2,): raise TypeError('Omega : shape is ' + str(omega.shape) + ' ((2,) expected)')

        C = np.zeros(2)

        d2 = self.m[1] * self.la[0] * self.lg[1]

        C[0] = -1 * omega[1] * (2. * omega[0] + omega[1]) * d2 * math.sin(theta[1])
        C[1] = omega[0]**2 * d2 * math.sin(theta[1])

        return C

    def G(self, theta):
        """Compute ??? matrix (???)"""
        if theta.shape != (2,): raise TypeError('Theta : shape is ' + str(theta.shape) + ' ((2,) expected)')

        G = np.zeros(2)

        G[0] = self.m[0] * self.g * self.lg[0] * math.cos(theta[0]) + self.m[1] * self.g * (self.la[0] * math.cos(theta[0] + self.lg[1] * math.cos(theta[0] + theta[1])))
        G[1] = self.m[1] * self.g * self.lg[1] * math.cos(theta[0] + theta[1])

        return G

    def getTheta(self):
        return (self.theta % (2 * math.pi)).tolist()

    def getOmega(self):
        return self.omega.tolist()

    def getAlpha(self):
        return self.alpha.tolist()

    def getTau(self):
        return self.tau.tolist()

    def getBonesLength(self):
        return self.la.tolist()

