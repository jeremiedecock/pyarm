# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from abstract_arm_model import AbstractArmModel
import math
import numpy as np

class ArmModel(AbstractArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane).

    References :
    [1] H. Kambara, K. Kim, D. Shin, M. Sato, and Y. Koike.
    "Learning and generation of goal-directed arm reaching from scratch."
    Neural Networks, 22(4):348-361, 2009. 
    """

    # CONSTANTS ###############################################################

    name = 'Kambara'

    # Bound values for assert ###################

    # Min and max joint angles (rd)
    angle_bounds = [
                    # Shoulder
                    {'min': math.radians(-140),
                     'max': math.radians(90)}, 

                    # Elbow
                    {'min': math.radians(0),
                     'max': math.radians(160)}
                   ] 

    # Initial joint angles
    initial_angles = [0., 0.]

    # Arm parameters ############################
    
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

    ###########################################################################

    def B(self, velocities):
        "Compute joint friction matrix."
        return np.zeros(2)

