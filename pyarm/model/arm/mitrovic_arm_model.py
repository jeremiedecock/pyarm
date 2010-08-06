# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.model.arm.abstract_arm_model import AbstractArmModel
import numpy as np

class ArmModel(AbstractArmModel):
    """Horizontally planar 2 DoF arm model.
    
    References :
    [0] Djordje Mitrovic
    http://www.ipab.informatics.ed.ac.uk/slmc/SLMCpeople/Mitrovic_D.html

    [1] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Adaptive Optimal Control for Redundantly Actuated Arms",
    Proc. Simulation of Adaptive Behavior (SAB), 2008
    
    [2] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Optimal Control with Adaptive Internal Dynamics Models",
    Proc. International Conference on Informatics in Control,
    Automation and Robotics (ICINCO), 2008

    [3] Djordje Mitrovic, Stefan Klanke, Rieko Osu, Mitsuo Kawato,
    and Sethu Vijayakumar, "Impedance Control as an Emergent Mechanism from
    Minimising Uncertainty", under review,  preprint, 2009

    [4] Djordje Mitrovic, Sho Nagashima, Stefan Klanke, Takamitsu Matsubara,
    and Sethu Vijayakumar, "Optimal Feedback Control for Anthropomorphic
    Manipulators", Accepted for ICRA, 2010

    [5] Djordje Mitrovic, Stefan Klanke, and Sethu Vijayakumar,
    "Exploiting Sensorimotor Stochasticity for Learning Control of Variable
    Impedance Actuators", under review, preprint available soon, 2010

    ---

    This model is based on [6] and [7]

    [6] M. Katayama and M. Kawato.
    "Virtual trajectory and stiffness ellipse during multijoint arm movement
    predicted by neural inverse models".
    Biological Cybernetics, 69(5):353-362, 1993.

    [7] Todorov & Li
    """

    # CONSTANTS ###############################################################

    name = 'Mitrovic'

    # Arm parameters from [6] p.356 ###########################################

    shoulder_inertia = 4.77E-2   # Moment of inertia at shoulder join (kg·m²)
    elbow_inertia = 5.88E-2      # Moment of inertia at elbow join (kg·m²)

    forearm_mass = 1.44          # Forearm mass (kg)

    upperarm_length = 0.3        # Upperarm length (m)
    forearm_length = 0.35        # Forearm length (m)

    # Distance from the forearm joint center to the forearm center of mass (m)
    forearm_cog = 0.21 

    ###########################################################################

    def B(self, velocities):
        "Compute joint friction matrix."
        return np.zeros(2)

    def G(self, angles):
        "Compute gravity force matrix."
        return np.zeros(2)

