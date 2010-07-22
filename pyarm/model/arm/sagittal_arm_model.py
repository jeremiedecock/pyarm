# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from kambara_arm_model import ArmModel as KambaraArmModel
import numpy as np

class ArmModel(KambaraArmModel):
    """Vertically planar 2 DoF arm model (sagittal plane) with gravity and
    friction.

    References :
    [1] H. Kambara, K. Kim, D. Shin, M. Sato, and Y. Koike.
    "Learning and generation of goal-directed arm reaching from scratch."
    Neural Networks, 22(4):348-361, 2009. 
    """

    # CONSTANTS ###############################################################

    name = 'Sagittal'

    # Arm parameters ##########################################################

    friction_matrix = np.array([[0.05, 0.025], [0.025, 0.05]])

    ###########################################################################

    def B(self, omega):
        "Compute joint friction matrix."
        return np.dot(self.friction_matrix, omega)

