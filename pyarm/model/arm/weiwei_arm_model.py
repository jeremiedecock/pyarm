# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.model.arm.abstract_arm_model import AbstractArmModel
import numpy as np

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model.
    
    References :
    [1] W. Li. "Optimal control for biological movement systems".
    PhD thesis, University of California, San Diego, 2006.
    """

    # CONSTANTS ###############################################################

    name = 'Li'

    # Arm parameters ##########################################################

    shoulder_inertia = 2.5E-2    # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 4.5E-2       # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.1           # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.33        # Upperarm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.16 

    ###########################################################################

    def G(self, angles):
        "Compute gravity force matrix."
        return np.zeros(2)

