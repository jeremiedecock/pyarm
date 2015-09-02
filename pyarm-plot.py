#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

plot3d = True
try:
    from mpl_toolkits.mplot3d import axes3d
except ImportError:
    # Matplotlib 0.98.1 (Debian Lenny)
    plot3d = False

import matplotlib.pyplot as plt
import numpy as np

def main():

    # Init
    from pyarm.model.muscle import kambara_muscle_model
    from pyarm.model.muscle import mitrovic_muscle_model
    from pyarm.model.muscle import weiwei_muscle_model

    from pyarm.model.arm import kambara_arm_model
    from pyarm.model.arm import mitrovic_arm_model
    from pyarm.model.arm import weiwei_arm_model

    kambara_arm  = kambara_arm_model.ArmModel()
    mitrovic_arm = mitrovic_arm_model.ArmModel()
    weiwei_arm   = weiwei_arm_model.ArmModel()

    kambara_muscle  = kambara_muscle_model.MuscleModel()
    mitrovic_muscle = mitrovic_muscle_model.MuscleModel()
    weiwei_muscle   = weiwei_muscle_model.MuscleModel()

    # Plot
    plot_muscle_length(kambara_arm, kambara_muscle)
    plot_muscle_length(mitrovic_arm, mitrovic_muscle)

    plot_stiffness(kambara_muscle)
    plot_stiffness(mitrovic_muscle)

    plot_viscosity(kambara_muscle)
    plot_viscosity(mitrovic_muscle)

    plot_lr(kambara_muscle)
    plot_lr(mitrovic_muscle)

    plot_nf(weiwei_muscle)
    plot_fe(weiwei_muscle)
    plot_fl(weiwei_muscle)

    if plot3d:
        plot_fv(weiwei_muscle)
        plot_fa(weiwei_muscle)

        plot_c_forearm(kambara_arm)
        plot_c_forearm(mitrovic_arm)
        
        # Plot 4d
        plot_c_upperarm(mitrovic_arm)


def plot_muscle_length(arm, muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    qmin = min(arm.angle_constraints[0]['min'], arm.angle_constraints[1]['min'])
    qmax = max(arm.angle_constraints[0]['max'], arm.angle_constraints[1]['max'])
    q = np.linspace(qmin, qmax, n)

    lm = np.zeros([len(q), 6])
    for i, qi in enumerate(q):
        arm.angles = np.ones(2) * qi
        arm.angles = arm.constraint_joint_angles(arm.angles)
        lm[i] = muscle.muscle_length(arm.angles)

    # Plot data #################
    plt.xlabel('Angle (rad)')
    plt.ylabel('Muscle length (m)')
    plt.title(muscle.name)
    plt.plot(q, lm)
    try:
        plt.legend(muscle.muscles, loc='best', prop={'size':'x-small'})
    except AttributeError:
        # Matplotlib 0.98.1 (Debian Lenny)
        plt.legend(muscle.muscles, loc='best')

    plt.savefig('muscle_' + muscle.name + '_lm.png')

def plot_stiffness(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    k = np.zeros([len(u), 6])
    for i, ui in enumerate(u):
        k[i] = muscle.stiffness(np.ones(6) * ui)

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Muscle stiffness (N/m)')
    plt.title(muscle.name)
    plt.plot(u, k)
    try:
        plt.legend(muscle.muscles, loc='best', prop={'size':'x-small'})
    except AttributeError:
        # Matplotlib 0.98.1 (Debian Lenny)
        plt.legend(muscle.muscles, loc='best')

    plt.savefig('muscle_' + muscle.name + '_k.png')

def plot_viscosity(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    b = np.zeros([len(u), 6])
    for i, ui in enumerate(u):
        b[i] = muscle.viscosity(np.ones(6) * ui)

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Muscle viscosity (N.s/m)')
    plt.title(muscle.name)
    plt.plot(u, b)
    try:
        plt.legend(muscle.muscles, loc='best', prop={'size':'x-small'})
    except AttributeError:
        # Matplotlib 0.98.1 (Debian Lenny)
        plt.legend(muscle.muscles, loc='best')

    plt.savefig('muscle_' + muscle.name + '_v.png')

def plot_lr(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    rl = np.zeros([len(u), 6])
    for i, ui in enumerate(u):
        rl[i] = muscle.rest_length(np.ones(6) * ui)

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Muscle rest length (m)')
    plt.title(muscle.name)
    plt.plot(u, rl)
    try:
        plt.legend(muscle.muscles, loc='best', prop={'size':'x-small'})
    except AttributeError:
        # Matplotlib 0.98.1 (Debian Lenny)
        plt.legend(muscle.muscles, loc='best')

    plt.savefig('muscle_' + muscle.name + '_lr.png')

def plot_nf(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(0.1, 0.7, n)

    nf = muscle.nf(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('nf (?)')
    plt.title(muscle.name)
    plt.plot(lm, nf)

    plt.savefig('muscle_' + muscle.name + '_nf.png')

def plot_fe(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(0.1, 0.7, n)

    fe = muscle.fe(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('Elastic force')
    plt.title(muscle.name)
    plt.plot(lm, fe)

    plt.savefig('muscle_' + muscle.name + '_fe.png')

def plot_fl(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(0.1, 0.7, n)

    fl = muscle.fl(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('Force-length relationship')
    plt.title(muscle.name)
    plt.plot(lm, fl)

    plt.savefig('muscle_' + muscle.name + '_fl.png')


def plot_fv(muscle):

    # Build datas ###############
    n = 50
    x = np.linspace(0.1, 0.7, n)
    y = np.linspace(0., 1.5, n)

    z = np.zeros([len(x), len(y)])
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = muscle.fv(np.ones(6) * xi, np.ones(6) * yj)[0]

    x, y = np.meshgrid(x, y)

    # Plot data #################
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Muscle length (m)')
    ax.set_ylabel('Muscle velocity (m/s)')
    ax.set_zlabel('Force-velocity relationship')

    plt.savefig('muscle_' + muscle.name + '_fv.png')


def plot_fa(muscle):

    # Build datas ###############
    n = 50
    x = np.linspace(0.1, 0.7, n)
    y = np.linspace(0., 1., n)

    z = np.zeros([len(x), len(y)])
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = muscle.fa(xi, yj)

    x, y = np.meshgrid(x, y)

    # Plot data #################
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Muscle length (m)')
    ax.set_ylabel('Motor signal')
    ax.set_zlabel('Activation-frequency relationship')

    plt.savefig('muscle_' + muscle.name + '_fa.png')


def plot_c_forearm(arm):

    # Build datas ###############
    n = 50
    x = np.linspace(arm.angle_constraints[1]['min'],
                    arm.angle_constraints[1]['max'], n)
    y = np.linspace(arm.bounds['angular_velocity']['min'],
                    arm.bounds['angular_velocity']['max'], n)

    z = np.zeros([len(x), len(y)])
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = arm.C(np.array([0, xi]), np.array([yj, 0]))[1]

    x, y = np.meshgrid(x, y)

    # Plot data #################
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Elbow joint angle (rad)')
    ax.set_ylabel('Shoulder velocity (rad/s)')
    ax.set_zlabel('Centrifugal, coriolis and friction forces applied on forearm')

    plt.savefig('arm_' + arm.name + '_c_forearm.png')

    
def plot_c_upperarm(arm):
    
    # Build datas ###############
    n  = 50
    nf = 10

    qe = np.linspace(arm.angle_constraints[1]['min'] + 0.1, # Fails if = 0...
                     arm.angle_constraints[1]['max'], nf)

    for t, qet in enumerate(qe):

        qps = np.linspace(-10., 10., n)
        qpe = np.linspace(-10., 10., n)
        #qps = np.linspace(arm.bounds['angular_velocity']['min'],
        #                 arm.bounds['angular_velocity']['max'], n)
        #qpe = np.linspace(arm.bounds['angular_velocity']['min'],
        #                 arm.bounds['angular_velocity']['max'], n)

        z = np.zeros([len(qps), len(qpe)])
        for i, qpsi in enumerate(qps):
            for j, qpej in enumerate(qpe):
                z[j, i] = arm.C(np.array([0, qet]), np.array([qpsi, qpej]))[0]

        qps, qpe = np.meshgrid(qps, qpe)

        # Plot data #################
        fig = plt.figure()
        ax = axes3d.Axes3D(fig)
        ax.cla()

        ax.plot_wireframe(qps, qpe, z)

        ax.set_xlabel('Elbow joint angle (rad)')
        ax.set_ylabel('Shoulder velocity (rad/s)')
        ax.set_zlabel('Centrifugal, coriolis and friction forces applied on forearm')

        plt.savefig('c_upperarm_' + str(t) + '.png')

if __name__ == '__main__':
    main()

